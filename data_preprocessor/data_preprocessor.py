import ast
import glob
import re
from pathlib import Path
import astor
import pandas as pd
import spacy
from tqdm import tqdm
from nltk.tokenize import RegexpTokenizer
from sklearn.model_selection import train_test_split
import sys
sys.path.append('../')
from utils.general_utils import apply_parallel, flattenlist

def tokenize_docstring(text):
    "Apply tokenization using spacy to docstrings."
    EN = spacy.load('en')
    tokens = EN.tokenizer(text)
    return [token.text.lower() for token in tokens if not token.is_space]


def tokenize_code(text):
    "A very basic procedure for tokenizing code strings."
    return RegexpTokenizer(r'\w+').tokenize(text)


def get_function_docstring_pairs(blob):
    "Extract (function/method, docstring) pairs from a given code blob."
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
                          ' '.join(tokenize_code(function)),
                          ' '.join(tokenize_docstring(docstring.split('\n\n')[0]))
                         ))
    except (AssertionError, MemoryError, SyntaxError, UnicodeEncodeError):
        pass
    return pairs


def get_function_docstring_pairs_list(blob_list):
    """apply the function `get_function_docstring_pairs` on a list of blobs"""
    return [get_function_docstring_pairs(b) for b in blob_list]


def listlen(x):
    if not isinstance(x, list):
        return 0
    return len(x)


def write_to(df, filename, path):
    "Helper function to write processed files to disk."
    out = Path(path)
    out.mkdir(exist_ok=True)
    df.function_tokens.to_csv(out/'{}.function'.format(filename), index=False)
    df.original_function.to_json(out/'{}_original_function.json.gz'.format(filename), orient='values', compression='gzip')
    # if filename != 'without_docstrings':
    #     df.docstring_tokens.to_csv(out/'{}.docstring'.format(filename), index=False)
    df.url.to_csv(out/'{}.lineage'.format(filename), index=False)


def process_data(raw_data_path, outfile_path):
    print('\nProcessing data...\n')

    loadpath = Path(raw_data_path)
    df = pd.read_csv(loadpath/'cc_raw_data.csv')

    df['nwo'] = df['repo_path'].apply(lambda r: r.split()[0])
    df['path'] = df['repo_path'].apply(lambda r: r.split()[1])
    df.drop(columns=['repo_path'], inplace=True)
    df = df[['nwo', 'path', 'content']]
    df.head()

    # Inspect shape of the raw data
    df.shape

    pairs = flattenlist(apply_parallel(get_function_docstring_pairs_list, df.content.tolist(), cpu_cores=4))

    assert len(pairs) == df.shape[0], f'Row count mismatch. `df` has {df.shape[0]:,} rows; `pairs` has {len(pairs):,} rows.'
    df['pairs'] = pairs
    df.head()


    # flatten pairs
    df = df.set_index(['nwo', 'path'])['pairs'].apply(pd.Series).stack()
    df = df.reset_index()
    df.columns = ['nwo', 'path', '_', 'pair']


    df['function_name'] = df['pair'].apply(lambda p: p[0])
    df['lineno'] = df['pair'].apply(lambda p: p[1])
    df['original_function'] = df['pair'].apply(lambda p: p[2])
    df['function_tokens'] = df['pair'].apply(lambda p: p[3])
    df['docstring_tokens'] = df['pair'].apply(lambda p: p[4])
    df = df[['nwo', 'path', 'function_name', 'lineno', 'original_function', 'function_tokens', 'docstring_tokens']]
    df['url'] = df[['nwo', 'path', 'lineno']].apply(lambda x: '/{}#L{}'.format(x[1], x[2]), axis=1)
    df.head()


    # remove observations where the same function appears more than once
    before_dedup = len(df)
    df = df.drop_duplicates(['original_function', 'function_tokens'])
    after_dedup = len(df)

    print(f'Removed {before_dedup - after_dedup:,} duplicate rows')

    df.shape

    print(f'All functions rows {df.shape[0]:,}')

    write_to(df, 'all_functions', outfile_path)
