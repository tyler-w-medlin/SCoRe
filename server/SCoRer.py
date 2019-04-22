import ast
import astor
from keras.backend import clear_session
#these import locations will likely change
import numpy as np
from code_summarizer import summarize_function
from language_encoder import encode

class SCoRer(object):
    def __init__(self,
                 code_summarizer,
                 lang_encoder,
                 search_index,
                 graph):

        self.code_summarizer = code_summarizer
        self.lang_encoder = lang_encoder
        self.search_index = search_index
        self.graph = graph

    def search(self, str_search, k=3):  # k is number of search results returned
        """
            searches database using input search string. Returns top 3 most
            relevant results and their corresponding keywords, and the cosine
            distance between the search string and results

            Input: search string, number of results to return [default 3]
            Return:
            Output: Prints search string, keywords, result docstring, cosine distance between them
        """
        query = self.lang_encoder.emb_mean(self.lang_encoder.get_keywords(str_search)).astype(np.float64)
        idxs, dists = self.search_index.knnQuery(query, k=k)

        return (idxs, dists)

    def prep_code(self, *args, file=False):
        """
        Switches based on arguments. 4 cases - Only a code snippet is passed; A file is passed;
        Both a code snippet and docstring are passed; and a default invalid case.
        Case 1 it summarizes the code snippet and vectorizes the resulting docstring
        Case 2 the file is parsed for function docstring pairs and summarizes/vectorizes functions and docstrings
        Case 3 the docstring is vectorized
        Case 4 prints invalid mode and the passed args

        Input: Case 1 - string containing code snippet; Case 2 - file, file=True;
        Case 3 - string containing code snippet, string containing docstring; Case 4 - anything else

        Return: Case 1 - code snippet dictionary { "code_snippet":, "docstring":, "vectorization":}
                Case 2 - list of code snippet dictionaries [{ "code_snippet":, "docstring":, "vectorization":}, ...]
                Case 3 - code snippet dictionary { "code_snippet":, "docstring":, "vectorization":}
                Case 4 - None
        """

        with self.graph.as_default():
            if len(args) == 1 and isinstance(args[0], str) and file == False:
                #CASE code snippet, no docstring
                emb, docstring = self.code_summarizer.predict(args[0])
                vectorization = self.lang_encoder.emb_mean(docstring)
                data_dict =	{
                    "code_snippet": args[0],
                    "docstring": docstring,
                    "vectorization": vectorization
                    }
                return [data_dict]

            elif len(args) == 1 and isinstance(args[0], str) and file == True:
                #CASE file is uploaded
                data_dict_list = []

                #unpack file
                #blob = args[0].unpack()
                #raw_data_dict_list = prepro(blob[0]) #unpack returns a single element tuple so an index is required

                #temporary way of loading a blob of code until file io is up
                raw_data_dict_list = self.prepro(args[0])
                
                for dict in raw_data_dict_list:
                    #generate docstring if the function doesn't have one
                    if dict["docstring"] == '':
                        #emb, dict["docstring"] = self.code_summarizer.predict(dict["raw_code"])
                        dict["docstring"] = summarize_function(self.code_summarizer, dict["raw_code"])
                    #vectorize docstring
                    vectorization = self.lang_encoder.emb_mean(dict["docstring"])
                    #append the new dict to the list of dictionaries
                    data_dict_list.append({
                        "code_snippet": dict["raw_code"],
                        "docstring": dict["docstring"],
                        "vectorization": vectorization
                        })

                return data_dict_list

            elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
                #CASE code snippet and string
                #vectorize docstring
                vectorization = self.lang_encoder.emb_mean(args[1])

                data_dict =	{
                    "code_snippet": args[0],
                    "docstring": args[1],
                    "vectorization": vectorization
                    }

                return [data_dict]

            else:
                print("\nInvalid args to prep_code() args = ", args)

    def prepro(self, blob):
        """
        Parses out function docstring pairs from file, then summarizes functions without docstrings
        and packages code snippet data in a list of dictionaries.
        Input: string containing python file
        Return: list of code snippet dictionaries { "raw_code":, "docstring":}
        """

        data_dict_list = []
        pairs = self.get_function_docstring_pairs(blob)
        for pair in pairs:
            pair = list(pair)
            if len(str(pair[4]).split()) < 3:
                pair[4] = ''
            data_dict_list.append({
                "raw_code": str(pair[3]),
                "docstring": str(pair[4])
                })

        return data_dict_list

    def get_function_docstring_pairs(self, blob):
        """
        Extract (function/method, docstring) pairs from a given code blob.
        Input: string containing python file
        Return: function/docstring pairs
        """
        pairs = []
        try:
            module = ast.parse(blob)
            classes = [node for node in module.body if isinstance(node, ast.ClassDef)]
            functions = [node for node in module.body if isinstance(node, ast.FunctionDef)]
            for _class in classes:
                functions.extend([node for node in _class.body if isinstance(node, ast.FunctionDef)])
            for f in functions:
                source = astor.to_source(f)
                docstring = ast.get_docstring(f) if ast.get_docstring(f) else ''
                function = source.replace(ast.get_docstring(f, clean=False), '') if docstring else source

                pairs.append((f.name,
                              f.lineno,
                              source,
                              ''.join(function),
                              ''.join(docstring.split('\n\n')[0])
                             ))
        except (AssertionError, MemoryError, SyntaxError, UnicodeEncodeError):
            pass
        return pairs
