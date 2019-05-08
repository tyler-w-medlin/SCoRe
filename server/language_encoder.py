"""
Language encoder - loads the model, encodes input strings

Author: Tristin Cory
"""

import sys
sys.path.append('./')
from tools.lang_model_utils import load_lm_vocab, Query2Emb, get_embeddings
import torch
import numpy as np
from pathlib import Path
import logging
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


def load_encoder(vocab_path, lang_model_path):
    """
    Loads the language encoder for embedding strings

    Input: path to vocab, path to language model

    Returns: Query2Emb object

    """
    #load vocab
    logging.warning('Loading vocab...')

    vocab = load_lm_vocab(os.path.join(THIS_FOLDER, vocab_path + '/vocab_v2.cls'))

    #load model
    logging.warning('Loading language model...')
    lang_model = torch.load(os.path.join(THIS_FOLDER, lang_model_path + '/lang_model_cpu_v2.torch'),
                            map_location=lambda storage, loc: storage)

    #create a language encoder object
    lang_encoder = Query2Emb(lang_model = lang_model.cpu(), vocab = vocab)

    return lang_encoder


def encode(lang_encoder, input_string):
    """
    Reads in a string and returns the embedding

    Input: Query2Emb object, input string

    Returns: string embedding

    """
    return lang_encoder.emb_mean(input_string)
