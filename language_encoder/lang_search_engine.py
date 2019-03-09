"""
This is a simple search engine base for interacting with the langauge encoder.
REQUIRED:
    - Precompiled search index
    - Trained language model
    - Reference data?
"""
import sys 
sys.path.append('../')
import nmslib
from lang_model_utils import Query2Emb
from lang_model_utils import load_lm_vocab
import torch
import nltk 
from nltk.corpus import stopwords

# These must only be run once on your system then they can be commented out to save time
nltk.download('stopwords') 
nltk.download('punkt')

with open('../data/processed_data/test.docstring', 'r') as f: 
    test_raw = f.readlines() #Reference data

dim500_avg_searchindex = nmslib.init(method='hnsw', space='cosinesimil')
dim500_avg_searchindex.loadIndex('../data/lang_model_emb/new_dim500_avg_searchindex.nmslib')
lang_model = torch.load('../data/lang_model/lang_model_cpu_v2.torch',map_location=lambda storage, loc: storage)
vocab = load_lm_vocab('../data/lang_model/vocab_v2.cls')

q2emb = Query2Emb(lang_model = lang_model.cpu(),vocab = vocab)

class search_engine:
    def __init__(self, 
                 nmslib_index, 
                 ref_data, 
                 query2emb_func):
        
        self.search_index = nmslib_index
        self.data = ref_data
        self.query2emb_func = query2emb_func
    
    def search(self, str_search, k=3): #k is number of search results returned
        query = self.query2emb_func.emb_mean(str_search)
        idxs, dists = self.search_index.knnQuery(query, k=k)
        
        for idx, dist in zip(idxs, dists):
            print('Input string:', str_search, '\nKeywords:', self.query2emb_func.get_keywords(str_search), '\nResult:', self.data[idx], f'cosine dist:{dist:.4f}\n---------------\n')

se = search_engine(nmslib_index = dim500_avg_searchindex,
                   ref_data = test_raw,
                   query2emb_func = q2emb)

se.search('read csv into pandas dataframe')