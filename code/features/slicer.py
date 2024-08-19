import matplotlib.pyplot as plt

def parse_conll(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    ln = 0
    pos_tags = []
    position = []
    feats = []
    for line in lines:
        ln += 1
        if line.strip():
            parts = line.split('\t')
            if len(parts) > 1 and parts[3] != 'PUNCT':
                pos_tags.append(parts[4])
                feats.append(parts[5])
                position.append(ln)
    return position, pos_tags, feats

def calculate_window_value(position, pos_tags, feats, window_size=200):
    results = []
    max_value = 0
    min_value = 1
    for i in range(0, len(pos_tags) - window_size + 1):
        window = pos_tags[i:i + window_size]
        
        cat1 = sum(1 for j in range(i, i + window_size) if pos_tags[j].startswith("V") and pos_tags[j].endswith("FIN") and 'Mood=Sub' in feats[j] and 'Tense=Past' in feats[j])
        cat2 = sum(1 for j in range(i, i + window_size) if pos_tags[j].startswith("V") and pos_tags[j].endswith("FIN"))
        cat3 = sum(1 for j in range(i, i + window_size) if pos_tags[j].startswith("VV"))
        cat4 = sum(1 for j in range(i, i + window_size) if pos_tags[j].startswith("V") and not pos_tags[j].startswith("VV"))
        
        details = [cat1, cat2, cat3, cat4]

        ratio = cat1 / cat2 * cat3 / cat4 if cat2 != 0 and cat4 != 0 else 0
        
        adja_count = window.count('ADJA')
        nn_count = window.count('NN')
        ratio = adja_count / nn_count if nn_count != 0 else 0
        
        if ratio > max_value:
            max_value = ratio
            position_max = (position[i], position[i + window_size - 1])
            details_max = details
            window_max = window
        if ratio < min_value:
            min_value = ratio
            position_min = (position[i], position[i + window_size - 1])
        results.append(ratio)
    print(f'Maximum ratio: {max_value} at position {position_max}')
    print(f'Details: {details_max}')
    print(f'Window: {window_max}')
    print(f'Minimum ratio: {min_value} at position {position_min}')
    return results

def main(file_path):
    position, pos_tags, feats = parse_conll(file_path)
    ratios = calculate_window_value(position, pos_tags, feats)
    return ratios

if __name__ == "__main__":
    file_path = input("Enter the path to the txt file: ")
    ratios = main('../../corpus/'+file_path.replace('.txt', '.conllu'))
    
    # plot the ratios as a line plot which should be smoothed first
    
    plt.figure(figsize=(10, 6))
    plt.plot(ratios)
    plt.ylabel('Ratio of ADJA to NN')
    plt.xlabel('Window')
    plt.tight_layout()
    
    plt.savefig(f'adja_nn_ratio.png')

    #print statistics of the ratios
    #print('Mean:', sum(ratios) / len(ratios))
    #print('Median:', sorted(ratios)[len(ratios) // 2])
    #print('Max:', max(ratios)) 
    #print('Min:', min(ratios))     