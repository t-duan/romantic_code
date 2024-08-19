import pandas as pd
from datetime import datetime
from pathlib import Path
import time
import multiprocessing
from utils import *

def get_conllu_stats(conllu_path: str):
    parsed_sentences = parse_conllu(conllu_path)
    num_sentences = count_sentences(parsed_sentences)
    num_tokens = count_tokens(parsed_sentences)
    num_tokens_no_punct = count_tokens_no_punct(parsed_sentences)
    num_adja = count_pos(parsed_sentences, 'ADJA')
    num_nn = count_pos(parsed_sentences, 'NN')
    num_v = count_pos_v(parsed_sentences)
    num_vv = count_pos_vv(parsed_sentences)
    num_vfin = count_vfin(parsed_sentences)
    num_vvfin = count_pos(parsed_sentences, 'VVFIN')

    num_konj_vf = count_konj_vf(parsed_sentences)
    num_konj_vvf = count_konj_vvf(parsed_sentences)
    acc_list, dat_list = extract_cases(parsed_sentences)
    return conllu_path, num_sentences, num_tokens, num_tokens_no_punct, num_adja, num_nn, num_v, num_vv, num_vfin, num_vvfin, num_konj_vf, num_konj_vvf, acc_list, dat_list

def get_stat(csv_path: str, folder_path: str, num_cores: int):
    df = pd.read_csv(csv_path, sep='\t')
    
    conllu_files = [Path(folder_path) / text_path.replace('.txt', '.conllu') for text_path in df['textPath']]
    valid_files = [str(f) for f in conllu_files if f.is_file()]
    
    # Use a multiprocessing Pool to parallelize the file processing
    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.map(get_conllu_stats, valid_files)
    
    # Organize the results into the DataFrame
    stats_dict = {
        'n_sent': [],
        'n_tok': [],
        'n_tok_no_punct': [],
        'n_adja': [],
        'n_nn': [],
        'n_v': [],
        'n_vv': [],
        'n_vfin': [],
        'n_vvfin': [],
        'n_konj_vf': [],
        'n_konj_vvf': [],
        'n_acc': [],
        'n_dat': [],
        'n_acc_doppelt': [],
        'n_dat_doppelt': []
    }
    
    acc_dict = {}
    dat_dict = {}

    for file_path, n_sent, n_tok, n_tok_no_punct, n_adja, n_nn, n_v, n_vv, n_vfin, n_vvfin, n_konj_vf, n_konj_vvf, acc_list, dat_list in results:
        stats_dict['n_sent'].append(n_sent)
        stats_dict['n_tok'].append(n_tok)
        stats_dict['n_tok_no_punct'].append(n_tok_no_punct)
        stats_dict['n_adja'].append(n_adja)
        stats_dict['n_nn'].append(n_nn)
        stats_dict['n_v'].append(n_v)
        stats_dict['n_vv'].append(n_vv)
        stats_dict['n_vfin'].append(n_vfin)
        stats_dict['n_vvfin'].append(n_vvfin)
        stats_dict['n_konj_vf'].append(n_konj_vf)
        stats_dict['n_konj_vvf'].append(n_konj_vvf)

        stats_dict['n_acc'].append(len(acc_list))
        stats_dict['n_dat'].append(len(dat_list))

        n_acc_doppelt = 0
        n_dat_doppelt = 0
        for acc in acc_list:
            if acc in acc_dict:
                acc_dict[acc] += 1
            else:
                acc_dict[acc] = 1
        for acc_doppelt in acc_list:
            if acc_doppelt[1] in ['in','an', 'auf', 'unter', 'über', 'vor', 'zwischen']:
                n_acc_doppelt += 1

        for dat in dat_list:
            if dat in dat_dict:
                dat_dict[dat] += 1
            else:
                dat_dict[dat] = 1
        for dat_doppelt in dat_list:
            if dat_doppelt[1] in ['in','an', 'auf', 'unter', 'über', 'vor', 'zwischen']:
                n_dat_doppelt += 1
        
        stats_dict['n_acc_doppelt'].append(n_acc_doppelt)
        stats_dict['n_dat_doppelt'].append(n_dat_doppelt)

    acc_dict = dict(sorted(acc_dict.items(), key=lambda item: item[1], reverse=True))
    dat_dict = dict(sorted(dat_dict.items(), key=lambda item: item[1], reverse=True))
    
    df['n_sent'] = stats_dict['n_sent']
    df['n_tok'] = stats_dict['n_tok']
    df['n_tok_no_punct'] = stats_dict['n_tok_no_punct']
    df['n_adja'] = stats_dict['n_adja']
    df['n_nn'] = stats_dict['n_nn']
    df['n_v'] = stats_dict['n_v']
    df['n_vv'] = stats_dict['n_vv']
    df['n_vfin'] = stats_dict['n_vfin']
    df['n_vvfin'] = stats_dict['n_vvfin']
    df['n_konj_vf'] = stats_dict['n_konj_vf']
    df['n_konj_vvf'] = stats_dict['n_konj_vvf']
    df['n_acc'] = stats_dict['n_acc']
    df['n_dat'] = stats_dict['n_dat']
    df['n_acc_doppelt'] = stats_dict['n_acc_doppelt']
    df['n_dat_doppelt'] = stats_dict['n_dat_doppelt']

    return df, acc_dict, dat_dict

if __name__ == "__main__":

    csv_path = input("Enter the path to the CSV file: ")
    folder_path = '../corpus/'
    num_cores = int(input("Enter the number of cores to use: "))

    start_time = time.time()  # Start the timer for the whole script

    df, dict_acc, dict_dat = get_stat(csv_path, folder_path, num_cores)

    output_file = f"{csv_path[:-4]}_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(output_file, sep='\t', index=False)
    print(f"Output saved to {output_file}")
    
    # save dict_acc to a csv
    acc_df = pd.DataFrame(dict_acc.items(), columns=['acc', 'count'])
    acc_df.to_csv(f"{csv_path[:-4]}_acc_{datetime.now().strftime('%Y%m%d')}.csv", sep='\t', index=False)
    # sum up counts of accusative phrases
    acc_sum = sum(dict_acc.values())
    print(f"Total accusative phrases: {acc_sum}")
    
    # save dict_dat to a csv
    dat_df = pd.DataFrame(dict_dat.items(), columns=['dat', 'count'])
    dat_df.to_csv(f"{csv_path[:-4]}_dat_{datetime.now().strftime('%Y%m%d')}.csv", sep='\t', index=False)
    # sum up counts of dative phrases
    dat_sum = sum(dict_dat.values())
    print(f"Total dative phrases: {dat_sum}")

    end_time = time.time()  # End the timer for the whole script
    print(f"Total script processing time: {end_time - start_time:.2f} seconds")
