from keras.models import load_model
from pathlib import Path
import numpy as np
from data_init.utils.seq2seq_utils import load_text_processor

code2emb_path = Path('./data/code2emb/')
seq2seq_path = Path('./data/seq2seq/')
data_path = Path('./data/processed_data/')

code2emb_model = load_model(code2emb_path/'code2emb_model.hdf5')
num_encoder_tokens, enc_pp = load_text_processor(seq2seq_path/'py_code_proc_v2.dpkl')

with open(data_path/'without_docstrings.function', 'r') as f:
    no_docstring_funcs = f.readlines()

encinp = enc_pp.transform_parallel(no_docstring_funcs)

nodoc_vecs = code2emb_model.predict(encinp, batch_size=20000)


# make sure the number of output rows equal the number of input rows
assert nodoc_vecs.shape[0] == encinp.shape[0]

np.save(code2emb_path/'nodoc_vecs.npy', nodoc_vecs)