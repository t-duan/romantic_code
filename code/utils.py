
from typing import List

def parse_conllu(file_path: str):
    """
    Parses a CoNLL-U file and returns a list of sentences, each sentence is a list of token dictionaries.
    """
    sentences = []
    sentence = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                if sentence:
                    sentences.append(sentence)
                    sentence = []
            elif not line.startswith("#"):  # Ignore comment lines
                parts = line.split('\t')
                if len(parts) == 10:
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
        if sentence:  # Add the last sentence if not already added
            sentences.append(sentence)
    return sentences

def count_sentences(parsed_sentences: List[List[dict]]):
    return len(parsed_sentences)

def count_tokens(parsed_sentences: List[List[dict]]):
    return sum(len(sentence) for sentence in parsed_sentences)

def count_tokens_no_punct(parsed_sentences: List[List[dict]]):
    return sum(1 for sentence in parsed_sentences for token in sentence if token['upostag'] != "PUNCT")

def count_pos(parsed_sentences: List[List[dict]], pos: str):
    return sum(1 for sentence in parsed_sentences for token in sentence if token['xpostag'] == pos)

def count_pos_v(parsed_sentences: List[List[dict]]):
    return sum(1 for sentence in parsed_sentences for token in sentence if token['xpostag'].startswith("V"))

def count_pos_vv(parsed_sentences: List[List[dict]]):
    return sum(1 for sentence in parsed_sentences for token in sentence if token['xpostag'].startswith("VV"))

def count_vfin(parsed_sentences: List[List[dict]]):
    return sum(1 for sentence in parsed_sentences for token in sentence if token['xpostag'].startswith("V") and token['xpostag'].endswith("FIN"))

def count_konj_vf(parsed_sentences: List[List[dict]]):
    return sum(1 for sentence in parsed_sentences for token in sentence if token['xpostag'].startswith("V") and token['xpostag'].endswith("FIN") and 'Mood=Sub' in token['feats'] and 'Tense=Past' in token['feats'])

def count_konj_vvf(parsed_sentences: List[List[dict]]):
    return sum(1 for sentence in parsed_sentences for token in sentence if token['xpostag'] == "VVFIN" and 'Mood=Sub' in token['feats'] and 'Tense=Past' in token['feats'])

def extract_cases(parsed_sentences: List[List[dict]]):
    """
    Finds verbial phrases in the accusative case in a list of sentences parsed from a CoNLL-U file.
    """
    accusative_phrases = []
    dativ_phrases = []
    for sentence in parsed_sentences:
        for token in sentence:
            if token['upostag'] == 'VERB':
                for t_1 in sentence:
                    if t_1['upostag'] == 'ADP' and t_1['head'] == token['id']:
                        for t_2 in sentence:
                            if t_2['head'] == t_1['id']:
                                if 'Case=Acc' in t_2['feats']:
                                    accusative_phrase = (token['lemma'], t_1['lemma'], t_2['lemma'])
                                    accusative_phrases.append(accusative_phrase)
                                elif 'Case=Dat' in t_2['feats']:
                                    dativ_phrase = (token['lemma'], t_1['lemma'], t_2['lemma'])
                                    dativ_phrases.append(dativ_phrase)
    return accusative_phrases, dativ_phrases