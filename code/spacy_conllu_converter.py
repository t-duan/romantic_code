# spacy_conllu_converter.py

import spacy
from spacy.tokens import Doc

class SpacyConlluConverter:
    def __init__(self):
        # Load the German language model
        self.nlp = spacy.load("de_core_news_md")#, disable=["ner"])
        self.nlp.max_length = 5000000
        print(f"Loaded spaCy pipeline components: {self.nlp.pipe_names}")  # Print the pipeline
    
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
                # Get named entity information for the token
                if not onlytokenize:
                    ent_info = []
                    if token.ent_iob_ != 'O':
                        ent_info.append(token.ent_type_)  # Use token.i for sentence-level index
                    conllu_line = [
                        str(token.i + 1),        # ID
                        token.text,            # FORM
                        token.lemma_,           # LEMMA
                        token.pos_,            # UPOS
                        token.tag_,            # XPOS
                        str(token.morph) if token.morph else "_",  # FEATS (convert MorphAnalysis to string)
                        str(token.head.i + 1 if token.head != token else 0),  # HEAD
                        token.dep_,            # DEPREL
                        '_',                    # DEPS
                        f'{token.ent_iob_}-{ent_info}'     # MISC (Named Entity)
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

def renumber_token_ids(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f_in:
        data = f_in.read().strip().split('\n\n')  # Splitte den Text in Sätze auf

    new_data = []  # Liste für die neu nummerierten Sätze

    # Für jeden Satz
    for sentence in data:
        lines = sentence.split('\n')  # Zerlege den Satz in Zeilen
        new_lines = []  # Liste für die neu nummerierten Zeilen
        id_mapping = {}  # Mapping von alten zu neuen Token IDs

        # Neu nummeriere die Token IDs in jedem Satz und erstelle das Mapping
        for i, line in enumerate(lines, start=1):
            parts = line.split('\t')
            old_id = parts[0]
            new_id = str(i)
            id_mapping[old_id] = new_id
        
        for i, line in enumerate(lines, start=1):
            parts = line.split('\t')
            # Korrigiere die HEAD IDs
            parts[0] = str(i)
            parts[6] = str(id_mapping.get(parts[6], '0'))
            new_lines.append('\t'.join(parts))

        # Füge den neu nummerierten Satz zur Liste der neu nummerierten Daten hinzu
        new_data.append('\n'.join(new_lines))

    # Schreibe die neu nummerierten Sätze in die Ausgabedatei
    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write('\n\n'.join(new_data))

# use the modul from command line
if __name__ == "__main__":
    import sys
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    use_custom_tokenizer = sys.argv[3]
    converter = SpacyConlluConverter()
    converter.process_file(input_file_path, output_file_path, use_custom_tokenizer)