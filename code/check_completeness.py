import pandas as pd

def compare_last_five_lines(file1, file2):
    def get_last_five_lines(file):
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Removing trailing newlines and spaces
            lines = [line.split('\t')[1] for line in lines if line.strip() and line.split('\t')[1].isalpha()]
        return lines[-5:]
    
    # Get the last five lines from each file
    last_five_1 = get_last_five_lines(file1)
    last_five_2 = get_last_five_lines(file2)
    
    if last_five_1 != last_five_2:
        print(file1)
        print(last_five_1)
        print(last_five_2)
        input()

if __name__ == "__main__":
    # Example usage:
    csv_path = input('Enter the path to the csv file: ')
    folder_path = '../corpus/'
    df = pd.read_csv(csv_path, sep='\t')
    # get a list of "textPath"
    files = df['textPath'].tolist()
    for file in files:
        file1 = folder_path + file[:-3] + 'conllu'
        file2 = folder_path + file[:-3] + 'conllu_0'
        compare_last_five_lines(file1, file2)
