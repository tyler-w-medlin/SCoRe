import sys
sys.path.append('./utils')
from data_preprocessor.data_preprocessor import process_data
from code_summarizer.code_summarizer import load_summarizer, summarize_dataset
from language_encoder.language_encoder import load_encoder, encode, embed_dataset
from search_engine.search_engine import SearchEngine, load_se, build_search_index

LANG_MODEL_PATH = './data/lang_model'
LANG_MODEL_EMB_PATH = './data/lang_model_emb'
PROCESSED_DATA_PATH = './data/processed_data'
SEQ2SEQ_PATH = './data/seq2seq'
UNPROCESSED_DATA_PATH = './data/unprocessed_data'

# # These must only be run once on your system then they can be commented out to save time
# import nltk
# from nltk.corpus import stopwords
# nltk.download('stopwords')
# nltk.download('punkt')

#Step 1 preprocess raw code
process_data(UNPROCESSED_DATA_PATH, PROCESSED_DATA_PATH)

#Step 2 load load_summarizer
code_summarizer = load_summarizer(SEQ2SEQ_PATH, SEQ2SEQ_PATH)

#Step 3 summarize dataset
summarize_dataset(code_summarizer, PROCESSED_DATA_PATH, PROCESSED_DATA_PATH)


#Step 4 load language_encoder
lang_encoder = load_encoder(LANG_MODEL_PATH, LANG_MODEL_PATH)

#Step 5 embed dataset
embed_dataset(lang_encoder, PROCESSED_DATA_PATH, LANG_MODEL_EMB_PATH)

#Step 6 build search index
build_search_index(LANG_MODEL_EMB_PATH, LANG_MODEL_EMB_PATH)
