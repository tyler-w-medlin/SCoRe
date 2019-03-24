import sys
sys.path.append('./utils')
from data_preprocessor.data_preprocessor import process_data
from code_summarizer.code_summarizer import load_summarizer, summarize_dataset
from language_encoder.language_encoder import load_encoder, encode, embed_dataset
from search_engine.search_engine import SearchEngine, load_se, build_search_index

LANG_MODEL_PATH = './data/lang_model'
LANG_MODEL_EMB_PATH = './data/lang_model_emb'
PROCESSED_DATA_PATH = './data/processed_data'

#load lang_encoder
lang_encoder = load_encoder(LANG_MODEL_PATH, LANG_MODEL_PATH)

#create search engine object
se = load_se(LANG_MODEL_EMB_PATH, PROCESSED_DATA_PATH, PROCESSED_DATA_PATH, lang_encoder)

#search
srch_flag = True
while srch_flag == True:
    srch_str = str(input("\n==============================\nEnter search string: "))
    print("\n--- Results ---")
    se.search(srch_str)

    proceed_str = str(input("Continue searching? (y/n):"))
    if proceed_str == "n":
        srch_flag = False
