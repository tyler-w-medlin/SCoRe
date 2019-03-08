import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)

use_cache = True

# # Optional: you can set what GPU you want to use in a notebook like this.
# # Useful if you want to run concurrent experiments at the same time on different GPUs.
import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="1"

# This will allow the notebook to run faster
from pathlib import Path
from general_utils import get_step2_prerequisite_files, read_training_files
from keras.utils import get_file
import logging
OUTPUT_PATH = Path('./data/seq2seq/')
OUTPUT_PATH.mkdir(exist_ok=True)

use_cache = True

# you want to supply the directory where the files are from step 1.
train_code, holdout_code, train_comment, holdout_comment = read_training_files('./data/processed_data/')

# code and comment files should be of the same length.

assert len(train_code) == len(train_comment)
assert len(holdout_code) == len(holdout_comment)

from ktext.preprocess import processor

if not use_cache:
    code_proc = processor(hueristic_pct_padding=.7, keep_n=20000)
    t_code = code_proc.fit_transform(train_code)

    comment_proc = processor(append_indicators=True, hueristic_pct_padding=.7, keep_n=14000, padding ='post')
    t_comment = comment_proc.fit_transform(train_comment)

elif use_cache:
    logging.warning('Not fitting transform function because use_cache=True')

from seq2seq_utils import load_decoder_inputs, load_encoder_inputs, load_text_processor



encoder_input_data, encoder_seq_len = load_encoder_inputs(OUTPUT_PATH/'py_t_code_vecs_v2.npy')
decoder_input_data, decoder_target_data = load_decoder_inputs(OUTPUT_PATH/'py_t_comment_vecs_v2.npy')
num_encoder_tokens, enc_pp = load_text_processor(OUTPUT_PATH/'py_code_proc_v2.dpkl')
num_decoder_tokens, dec_pp = load_text_processor(OUTPUT_PATH/'py_comment_proc_v2.dpkl')
from seq2seq_utils import build_seq2seq_model

seq2seq_Model = build_seq2seq_model(word_emb_dim=800,
                                    hidden_state_dim=1000,
                                    encoder_seq_len=encoder_seq_len,
                                    num_encoder_tokens=num_encoder_tokens,
                                    num_decoder_tokens=num_decoder_tokens)

seq2seq_Model.summary()

from keras.models import Model, load_model
import pandas as pd
import logging

if use_cache:
    logging.warning('Not re-training function summarizer seq2seq model because use_cache=True')
    # Load model from url
    loc = './data/seq2seq/py_func_sum_v9_.epoch16-val2.55276.hdf5'
    seq2seq_Model = load_model(loc)

    # Load encoder (code) pre-processor from url
    loc = './data/seq2seq/py_code_proc_v2.dpkl'

    num_encoder_tokens, enc_pp = load_text_processor(loc)

    # Load decoder (docstrings/comments) pre-processor from url
    loc = './data/seq2seq/py_comment_proc_v2.dpkl'

    num_decoder_tokens, dec_pp = load_text_processor(loc)

from seq2seq_utils import Seq2Seq_Inference
import pandas as pd

seq2seq_inf = Seq2Seq_Inference(encoder_preprocessor=enc_pp,
                                 decoder_preprocessor=dec_pp,
                                 seq2seq_model=seq2seq_Model)

demo_testdf = pd.DataFrame({'code':holdout_code, 'comment':holdout_comment, 'ref':''})
seq2seq_inf.demo_model_predictions(n=2, df=demo_testdf)


# This will return a BLEU Score
seq2seq_inf.evaluate_model(input_strings=holdout_code,
                           output_strings=holdout_comment,
                           max_len=None)


seq2seq_Model.save(OUTPUT_PATH/'code_summary_seq2seq_model.h5')
