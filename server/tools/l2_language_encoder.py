from keras.models import load_model
from pathlib import Path
import tensorflow as tf
import os
import warnings
import sys
import numpy as np
import sys
sys.path.append('../utils')
from seq2seq_utils import load_text_processor

def load_code2emb(code2emb_path, seq2seq_path):
    """
    Loads the code2emb module.

    Input: Path to the model and preprocessor

    Returns: code2emb model and text preprocessor

    """
    tf.logging.set_verbosity('ERROR')
    os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
    warnings.filterwarnings("ignore")

    code2emb_model = load_model(code2emb_path)
    num_encoder_tokens, enc_pp = load_text_processor(seq2seq_path)

    return LevelTwo(code2emb_model, enc_pp)

def code2emb(code, code2emb_model, enc_pp):
    """
    Vectorizes code snippet.

    Input: Code snippet, code2emb model, text preprocessor

    Returns: vectorization of input code snippet

    """
    lst = {code}
    encinp = enc_pp.transform_parallel(lst)

    vectorization = code2emb_model.predict(encinp, batch_size=20000)

    return vectorization

class LevelTwo:

    def __init__(self, code2mb_model, enc_pp):
        self.enc_pp = enc_pp
        self.code2emb_model = code2mb_model
    
    def code2emb(self, code):
        lst = {code}
        encinp = self.enc_pp.transform_parallel(lst)

        vectorization = self.code2emb_model.predict(encinp, batch_size=20000)
    
        return vectorization