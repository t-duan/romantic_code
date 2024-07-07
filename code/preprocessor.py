import os
import pandas as pd
from multiprocessing import Pool
from spacy_conllu_converter import SpacyConlluConverter
from spacy_conllu_converter import renumber_token_ids
from cab_normalizer import FileNormalizer

# Initialize the SpacyConlluConverter
converter = SpacyConlluConverter()
# Initialize the FileNormalizer
processor = FileNormalizer()

def process_files(args):
    plain_0_file_path, conllu_0_file_path, plain_1_file_path, conllu_1_file_path = args
    # Process the first plain text file to conllu format
    
    print(f'processing {plain_0_file_path}')
    converter.process_file(plain_0_file_path, conllu_0_file_path, use_custom_tokenizer=False)
    
    # Normalize the conllu file and return normalized plain text
    processor.split_process_combine(conllu_0_file_path, plain_1_file_path)
    
    # Process the normalized plain text file to conllu format
    converter.process_file(plain_1_file_path, conllu_1_file_path, use_custom_tokenizer=True)

    renumber_token_ids(conllu_1_file_path,conllu_1_file_path)

def get_file_paths_from_csv(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path, sep="\t")
    
    # Check if the 'file' column exists
    if 'textPath' not in df.columns:
        raise ValueError("The specified CSV file does not contain a 'textPath' column.")
    
    # Extract the file paths from the 'file' column and convert to a list
    file_paths = df['textPath'].tolist()
    
    return file_paths

folder_path = "../corpus/"
metadata = input("Enter the path to the metadata file: ")
files = get_file_paths_from_csv(metadata)

# add all lines in "../corpus/errorlist.txt" to the list of files
#files = []
#with open("../corpus/errorlist.txt") as f:
#    for file in f.readlines():
#        files.append(file.strip())

# Prepare arguments for parallel processing
args_list = []
for f in files:
    plain_0_file_path = folder_path + f
    conllu_0_file_path = plain_0_file_path[:-3] + 'conllu_0'
    plain_1_file_path = plain_0_file_path[:-3] + 'txt_1'
    conllu_1_file_path = plain_0_file_path[:-3] + 'conllu'
    #if not os.path.exists(conllu_1_file_path):
    #    print(plain_0_file_path)
    args_list.append((plain_0_file_path, conllu_0_file_path, plain_1_file_path, conllu_1_file_path))

# Define the number of CPU cores to use
num_cores = 6

# Create a multiprocessing pool with the specified number of cores
with Pool(num_cores) as pool:
    # Map the process_files function to each set of arguments
    # This will distribute the work among the available CPU cores
    pool.map(process_files, args_list)
