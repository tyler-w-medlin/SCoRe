import sys
from tools.general_utils import create_nmslib_search_index
import nmslib
from pathlib import Path
import numpy as np
import nltk
from nltk.corpus import stopwords

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
                 docstring_data,
                 function_data,
                 query2emb):

        self.search_index = nmslib_index
        self.docstring_data = docstring_data
        self.function_data = function_data
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
            '\nResult:', self.docstring_data[idx], f'cosine dist:{dist:.4f}\n','\nFunction: \n---------------\n',
            self.function_data[idx], '\n\n---------------\n')
            
            

def load_se(datasetidx_path, docstring_data_path, function_data_path, lang_encoder):
    """
        Load the search engine. reads in docstring/function data, parses out original
        functions, and takes a language encoder object as input.

        Input: path to folder containing dataset index, path to folder containing docstring data,
        path to folder containing original function data, Query2Emb object
        Return: SearchEngine object
    """
    dataset_searchindex = nmslib.init(method='hnsw', space='cosinesimil')
    dataset_searchindex.loadIndex(datasetidx_path + '/dataset_searchindex.nmslib')

    with open(docstring_data_path + '/generated_docstrings.docstring', 'r') as f:
        generated_docstrings = f.readlines() #docstring data

    with open(function_data_path + '/all_functions_original_function.json', 'r') as f:
        function_data_array = f.readlines() #function data

    function_data = ''
    #combine the lines read in from the json
    for line in function_data_array:
        function_data = function_data + line

    #replace escaped characters
    function_data = function_data.replace('\\n','\n')
    function_data = function_data.replace('\\t','\t')
    function_data = function_data.replace('\\"','\"')
    function_data = function_data.replace('\\/','/')
    function_data = function_data.split('\",\"')

    se = SearchEngine(nmslib_index = dataset_searchindex, docstring_data = generated_docstrings, function_data = function_data, query2emb = lang_encoder)

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
