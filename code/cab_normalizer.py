import tempfile
import os

class FileNormalizer:
    def __init__(self, max_lines=25000):
        self.max_lines = max_lines

    def process_file_part(self, part_path):
        """
        This function processes a single part of the file using the provided function.
        """
        os.system(f'bash cab-curl-xpost.sh "?a=default1.1700-1800&fmt=conllu" {part_path} -o {part_path + "_processed"}')

    def split_process_combine(self, input_file_path, output_file_path):
        """
        Splits the input file into chunks, processes each chunk, and combines the results.
        """
        temp_files = []

        with open(input_file_path, 'r') as file:
            current_part = []
            line_count = 0

            for line in file:
                line_count += 1
                current_part.append(line)

                if line_count > self.max_lines:
                    if line.strip() == '':  # Empty line found, end of part
                        temp_file_path = tempfile.NamedTemporaryFile(delete=False).name  # Create a temporary file
                        with open(temp_file_path, 'w') as temp_file:
                            temp_file.writelines(current_part)
                        temp_files.append(temp_file_path)

                        self.process_file_part(temp_file_path)

                        current_part = []  # Reset for the next part
                        print(f'Created part of {input_file_path}')
                        line_count = 0

        # Process any remaining lines
        if current_part:
            temp_file_path = tempfile.NamedTemporaryFile(delete=False).name
            with open(temp_file_path, 'w') as temp_file:
                temp_file.writelines(current_part)
            temp_files.append(temp_file_path)
            self.process_file_part(temp_file_path)

        # Combine processed parts into the output file
        with open(output_file_path, 'w') as outfile:
            for temp_file in temp_files:
                with open(temp_file + "_processed", 'r') as infile:  # Read from processed files
                    for line in infile:
                        if line == "":
                            outfile.write("\n")
                        else:
                            if not line.startswith("#"):
                                cab = line.strip().split("\t")[-1]
                                norm = cab.split('|')[-1][5:]
                                outfile.write(norm + "\n")
                os.remove(temp_file)  # Clean up temporary files
                os.remove(temp_file + "_processed")
