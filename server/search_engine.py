import sys
from tools.general_utils import create_nmslib_search_index
import nmslib
from pathlib import Path
import numpy as np
import nltk
from nltk.corpus import stopwords
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

class SearchEngine:
    """
        Search engine class
        Attributes: Search_index - index of database
                    docstring_data - docstring data for all functions
                    function_data - original function dataset
                    query2emb - object containing language encoder for encoding search strings
        Functions:  search() - searches database using input search string.
                               Returns top 3 most relevant results and their corresponding keywords,
                               and the cosine distance between the search string and results,
                               and prints the relevant function
    """
    def __init__(self,
                 nmslib_index,
                 query2emb):

        self.search_index = nmslib_index


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

        return (idxs, dists)


def load_se(datasetidx_path, lang_encoder):
    """
        Load the search engine. reads in docstring/function data, parses out original
        functions, and takes a language encoder object as input.

        Input: path to folder containing dataset index, path to folder containing docstring data,
        path to folder containing original function data, Query2Emb object
        Return: SearchEngine object
    """
    dataset_searchindex = nmslib.init(method='hnsw', space='cosinesimil')

    dataset_searchindex.loadIndex(os.path.join(THIS_FOLDER, datasetidx_path + '/dataset_searchindex.nmslib'))

    se = SearchEngine(nmslib_index = dataset_searchindex, query2emb = lang_encoder)

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
    dataset_searchindex = create_nmslib_search_index(dataset_embedding)

    # Save search index
    dataset_searchindex.saveIndex(search_index_path + '/dataset_searchindex.nmslib')
