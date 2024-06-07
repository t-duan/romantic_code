import os
import pandas as pd
from phonemizer import phonemize
from multiprocessing import Pool

def conllu_to_sentences(conllu_file, output_file):
    with open(conllu_file, 'r', encoding='utf-8') as f, open(output_file, 'w', encoding='utf-8') as out_f:
        sentence = []
        for line in f:
            if line.strip() == '':
                if sentence:
                    out_f.write(' '.join(sentence) + '\n')
                    sentence = []
            elif not line.startswith('#'):
                parts = line.split('\t')
                if len(parts) > 1:
                    sentence.append(parts[1])
        # Write the last sentence if exists
        if sentence:
            out_f.write(' '.join(sentence) + '\n')

def transcribe_sentences(input_file, output_file, language='de'):
    with open(input_file, 'r', encoding='utf-8') as f, open(output_file, 'w', encoding='utf-8') as out_f:
        text = f.read()
        transcription = phonemize(
            text,
            language=language,
            backend='espeak',
            strip=False,
            preserve_punctuation=True,
            with_stress=True
        )
        out_f.write(transcription)

def process_file(args):
    conllu_file, sentences_output_file, transcription_output_file = args
    # Convert CoNLL-U to sentences
    conllu_to_sentences(conllu_file, sentences_output_file)
    # Transcribe sentences
    transcribe_sentences(sentences_output_file, transcription_output_file)
    print(f"Processed {conllu_file} and saved sentences to {sentences_output_file}")
    print(f"Processed {conllu_file} and saved transcription to {transcription_output_file}")

def batch_process(files, num_processes=24):
    args_list = []
    for file in files:
        if file.endswith('.conllu_0'):
            sentences_file = file.replace('.conllu_0', '_sentences.txt')
            transcription_file = file.replace('.conllu_0', '_transcription.txt')
            args_list.append((file, sentences_file, transcription_file))
    
    with Pool(processes=num_processes) as pool:
        pool.map(process_file, args_list)

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

# Prepare arguments for parallel processing
files_to_process = []
for f in files:
#    if not os.path.exists(folder_path + f.replace('.txt','_transcription.txt')):
    files_to_process.append(folder_path + f.replace('.txt','.conllu_0'))

# Process all files in the list using 24 processes
batch_process(files_to_process, num_processes=8)
