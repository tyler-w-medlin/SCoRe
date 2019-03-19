import sys
sys.path.append('../')
from utils.general_utils import create_nmslib_search_index
import nmslib
from pathlib import Path
import numpy as np
import nltk
from nltk.corpus import stopwords

class SearchEngine:
    """
        Search engine class
        Attributes: Search_index - index of database
                    data - docstring data for all functions
                    query2emb - object containing language encoder for encoding search strings
        Functions:  search() - searches database using input search string.
                               Returns top 3 most relevant results and their corresponding keywords,
                               and the cosine distance between the search string and results
    """
    def __init__(self,
                 nmslib_index,
                 ref_data,
                 query2emb):

        self.search_index = nmslib_index
        self.data = ref_data
        self.query2emb = query2emb

    def search(self, str_search, k=3): #k is number of search results returned
        """
            searches database using input search string. Returns top 3 most
            relevant results and their corresponding keywords, and the cosine
            distance between the search string and results

            Input: search string, number of results to return [default 3]
            Return:
            Output: Prints search string, keywords, result docstring, cosine distance between them
        """
        query = self.query2emb.emb_mean(str_search)
        idxs, dists = self.search_index.knnQuery(query, k=k)

        for idx, dist in zip(idxs, dists):
            print('Input string:', str_search, '\nKeywords:', self.query2emb.get_keywords(str_search),
            '\nResult:', self.data[idx], f'cosine dist:{dist:.4f}\n---------------\n')

def load_se(datasetidx_path, ref_data_path, lang_encoder):
    dataset_searchindex = nmslib.init(method='hnsw', space='cosinesimil')
    dataset_searchindex.loadIndex(datasetidx_path + '/dataset_searchindex.nmslib')

    with open(ref_data_path + '/generated_docstrings.docstring', 'r') as f:
        generated_docstrings = f.readlines() #Reference data

    se = SearchEngine(nmslib_index = dataset_searchindex,
                        ref_data = generated_docstrings,
                        query2emb = lang_encoder)

    return se


def build_search_index(docstring_emb_path, search_index_path):
    """
        Build search index for database
        Input: Path to dataset embedding file, output path for search index file
        Return: -----
        Output: dataset search index file dataset_searchindex.nmslib
    """
    # Load matrix of vectors
    dataset_embedding = np.load(docstring_emb_path + '/dataset_embedding.npy') #docstring embeddings

    # Build search index
    # (takes about an hour on a p3.8xlarge)
    # ^ that is a dirty lie. You can do it. Just believe.
    dataset_searchindex = create_nmslib_search_index(dataset_embedding)

    # Save search index
    dataset_searchindex.saveIndex(search_index_path + '/dataset_searchindex.nmslib')
