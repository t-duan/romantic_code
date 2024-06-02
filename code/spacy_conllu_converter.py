# spacy_conllu_converter.py

import spacy
from spacy.tokens import Doc

class SpacyConlluConverter:
    def __init__(self):
        # Load the German language model
        self.nlp = spacy.load("de_core_news_md", disable=["ner"])
        self.nlp.max_length = 5000000
    
    def read_tokens(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            tokens = [line.strip() for line in file if line.strip()]
        return tokens

    def read_plain_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    def spacy_to_conllu(self, doc, onlytokenize):
        lines = []
        for sent in doc.sents:
            for i, token in enumerate(sent):
                # Generate CoNLL-U formatted line with phonetic transcription
                if not onlytokenize:
                    conllu_line = [
                        str(token.i + 1),        # ID
                        token.text,            # FORM
                        token.lemma_,           # LEMMA
                        token.pos_,            # UPOS
                        token.tag_,            # XPOS
                        str(token.morph) if token.morph else "_",  # FEATS (convert MorphAnalysis to string)
                        str(token.head.i + 1 if token.head != token else 0),  # HEAD
                        token.dep_,            # DEPREL
                        '_',
                        '_'
                    ]
                else:
                    conllu_line = [
                        str(token.i + 1),        # ID
                        token.text,
                        '_',
                        '_',
                        '_',
                        '_',
                        '_',
                        '_',
                        '_',
                        '_'
                    ]
                lines.append("\t".join(conllu_line))
            lines.append("")  # Sentence break
        return "\n".join(lines)

    def custom_tokenizer(self, tokens):
        # Create a Doc object with the provided tokens
        doc = Doc(self.nlp.vocab, words=tokens)
        return doc

    def process_file(self, input_file_path, output_file_path, use_custom_tokenizer=True):
        if use_custom_tokenizer:
            onlytokenize = False
            # Read tokens from the file
            tokens = self.read_tokens(input_file_path)
            doc = self.custom_tokenizer(tokens)
            doc = self.nlp(doc)
            conllu_output = self.spacy_to_conllu(doc,onlytokenize)
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(conllu_output)
        else:
            onlytokenize = True
            # Read the file as plain text
            text = self.read_plain_text(input_file_path).replace('\n',' ')
            doc = self.nlp(text)

            with open(input_file_path, "r", encoding="utf-8") as file, open(output_file_path, "w", encoding="utf-8") as out_file:
                for line in file:
                    line = line.strip()
                    if line:
                        doc = self.nlp(line)
                        conllu_data = self.spacy_to_conllu(doc,onlytokenize)
                        out_file.write(conllu_data + "\n")
