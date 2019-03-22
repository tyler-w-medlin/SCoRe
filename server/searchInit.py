# Cropped out by Elliott
def searchEngineInit():
    import sys
    # from data_preprocessor.data_preprocessor import process_data
    # from code_summarizer.code_summarizer import load_summarizer, summarize_dataset
    from language_encoder import load_encoder, encode, embed_dataset
    from search_engine import SearchEngine, load_se, build_search_index

    LANG_MODEL_PATH = 'tools/data/lang_model'
    LANG_MODEL_EMB_PATH = 'tools/data/lang_model_emb'
    PROCESSED_DATA_PATH = 'tools/data/processed_data'
    # SEQ2SEQ_PATH = './data/seq2seq'
    # UNPROCESSED_DATA_PATH = './data/unprocessed_data'

    #Step 4 load language_encoder
    lang_encoder = load_encoder(LANG_MODEL_PATH, LANG_MODEL_PATH)

    #Step 7 load search engine
    return load_se(LANG_MODEL_EMB_PATH, PROCESSED_DATA_PATH, PROCESSED_DATA_PATH, lang_encoder)
