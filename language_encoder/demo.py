from language_encoder import load_encoder, encode, embed_dataset

LANG_MODEL_PATH = '../data/lang_model'
LANG_MODEL_EMB_PATH = '../data/lang_model_emb'
PROCESSED_DATA_PATH = '../data/processed_data'
SEQ2SEQ_PATH = '../data/seq2seq'
UNPROCESSED_DATA_PATH = '../data/unprocessed_data'

input_docstring = "Connected to database"

#load the encoder model
lang_encoder = load_encoder(LANG_MODEL_PATH, LANG_MODEL_PATH)

print(f"\n****** Original Docstring ******\n {input_docstring}")

print(f"\n****** Docstring Embedding ******\n {encode(lang_encoder, input_docstring)}\n")

print("\n\n****** Embedding dataset ******\n")

embed_dataset(lang_encoder, PROCESSED_DATA_PATH, LANG_MODEL_EMB_PATH)
