import re
from typing import List, Tuple, Optional

def parse_conllu(file_path: str) -> List[List[dict]]:
    """
    Parses a CoNLL-U file and returns a list of sentences, each sentence is a list of token dictionaries.
    """
    sentences = []
    with open(file_path, 'r', encoding='utf-8') as file:
        sentence = []
        for line in file:
            line = line.strip()
            if not line:
                if sentence:
                    sentences.append(sentence)
                    sentence = []
            elif not line.startswith("#"):  # Ignore comment lines
                parts = line.split('\t')
                token = {
                    'id': parts[0],
                    'form': parts[1],
                    'lemma': parts[2],
                    'upostag': parts[3],
                    'xpostag': parts[4],
                    'feats': parts[5],
                    'head': parts[6],
                    'deprel': parts[7],
                    'deps': parts[8],
                    'misc': parts[9]
                }
                sentence.append(token)
        if sentence:
            sentences.append(sentence)
    return sentences

def count_sentences(file_path):
    return len(parse_conllu(file_path))

def count_tokens(file_path):
    return sum(len(sentence) for sentence in parse_conllu(file_path))

def count_tokens_no_punct(file_path):
    count = 0
    for sentence in parse_conllu(file_path):
        for token in sentence:
            if token['upostag'] != "PUNCT":
                count += 1
    return count

def count_adj(file_path):
    count = 0
    for sentence in parse_conllu(file_path):
        for token in sentence:
            if token['upostag'] == "ADJA":
                count += 1
    return count

def count_nn(file_path):
    count = 0
    for sentence in parse_conllu(file_path):
        for token in sentence:
            if token['upostag'] == "NN":
                count += 1
    return count

def find_accusative_phrases(sentences: List[List[dict]]) -> List[Tuple[str, List[str]]]:
    """
    Finds verbial phrases in the accusative case in a list of sentences parsed from a CoNLL-U file.
    """
    accusative_phrases = []
    for sentence in sentences:
        for token in sentence:
            # Look for tokens that are verbs (typically `VERB` in `upostag`)
            if token['upostag'] == 'VERB':
                # Collect the accusative objects and oblique arguments
                acc_objs = []
                for t in sentence:
                    # Check for accusative case in `feats` and relevant dependency relations
                    if re.search(r'Case=Acc', t['feats']):
                        if t['head'] == token['id'] and t['deprel'] in ('obj', 'obl:arg'):
                            acc_objs.append(t['form'])
                if acc_objs:
                    accusative_phrases.append((token['form'], acc_objs))
    return accusative_phrases

