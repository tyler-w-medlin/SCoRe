import logging
from pathlib import Path
from keras.models import Model, load_model
from seq2seq_utils import load_text_processor, Seq2Seq_Inference
import tensorflow as tf
import os
import warnings

def load_Summarizer():
    """
    Loads the code summarizer model and returns the interference object
    to be used for predicting docstrings.

    Input: -----

    Returns: Seq2Seq_Inference object

    """
    #the code from the GitHub team has a LOT of soon to be depricated functions
    #suppress the depricated warnings
    tf.logging.set_verbosity('ERROR')
    os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
    warnings.filterwarnings("ignore")

    OUTPUT_PATH = Path('../data/seq2seq/')
    OUTPUT_PATH.mkdir(exist_ok=True)
    OUTPUT_PATH = '../data/seq2seq/'

    logging.warning('Loading pre-trained model...')
    # Load model
    loc = OUTPUT_PATH + 'py_func_sum_v9_.epoch16-val2.55276.hdf5'
    seq2seq_Model = load_model(loc)

    logging.warning('Loading text processor (encoder)...')
    # Load encoder (code) pre-processor
    loc = OUTPUT_PATH + 'py_code_proc_v2.dpkl'
    num_encoder_tokens, enc_pp = load_text_processor(loc)

    logging.warning('Loading text processor (decoder)...')
    # Load decoder (docstrings/comments) pre-processor
    loc = OUTPUT_PATH + 'py_comment_proc_v2.dpkl'
    num_decoder_tokens, dec_pp = load_text_processor(loc)

    seq2seq_inf = Seq2Seq_Inference(encoder_preprocessor=enc_pp,
                                     decoder_preprocessor=dec_pp,
                                     seq2seq_model=seq2seq_Model)

    return seq2seq_inf

def summarize(seq2seq_inf, input_code):
        """
        Calls the predict() function on the Seq2Seq_Inference object
        to summarize the input code

        Input: Seq2Seq_Inference object, input code string

        Returns: predicted docstring

        """
        emb, gen_docstring = seq2seq_inf.predict(input_code)
        return gen_docstring
