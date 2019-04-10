# Cropped out by Elliott
def searchEngineInit():
    import sys
    # from data_preprocessor.data_preprocessor import process_data
    # from code_summarizer.code_summarizer import load_summarizer, summarize_dataset
    from language_encoder import load_encoder, encode, embed_dataset
    from code_summarizer import load_summarizer
    from SCoRer import SCoRer
    import nmslib
    
    LANG_MODEL_PATH = 'tools/data/lang_model'
    SEQ2SEQ_PATH = 'tools/data/seq2seq'
    # SEQ2SEQ_PATH = './data/seq2seq'
    # UNPROCESSED_DATA_PATH = './data/unprocessed_data'

    #Step 4 load language_encoder
    lang_encoder = load_encoder(LANG_MODEL_PATH, LANG_MODEL_PATH)
    code_summarizer = load_summarizer(SEQ2SEQ_PATH, SEQ2SEQ_PATH)
    dataset_searchindex = nmslib.init(method='hnsw', space='cosinesimil')
    dataset_searchindex.loadIndex('./dataset_searchindex.nmslib')

    #Step 7 load search engine
    return SCoRer(code_summarizer, lang_encoder, dataset_searchindex)
