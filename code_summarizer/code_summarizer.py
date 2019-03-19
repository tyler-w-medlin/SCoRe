import logging
from pathlib import Path
from keras.models import Model, load_model
import tensorflow as tf
import os
import warnings
import sys
sys.path.append('../')
from utils.seq2seq_utils import load_text_processor, Seq2Seq_Inference

def load_summarizer(seq2seq_model_path, text_processor_path):
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

    logging.warning('Loading pre-trained model...')
    # Load model
    seq2seq_Model = load_model(seq2seq_model_path + '/py_func_sum_v9_.epoch16-val2.55276.hdf5')

    logging.warning('Loading text processor (encoder)...')
    # Load encoder (code) pre-processor
    num_encoder_tokens, enc_pp = load_text_processor(text_processor_path + '/py_code_proc_v2.dpkl')

    logging.warning('Loading text processor (decoder)...')
    # Load decoder (docstrings/comments) pre-processor
    num_decoder_tokens, dec_pp = load_text_processor(text_processor_path + '/py_comment_proc_v2.dpkl')

    seq2seq_inf = Seq2Seq_Inference(encoder_preprocessor=enc_pp,
                                     decoder_preprocessor=dec_pp,
                                     seq2seq_model=seq2seq_Model)

    return seq2seq_inf

def summarize_function(seq2seq_inf, input_code):
    """
    Calls the predict() function on the Seq2Seq_Inference object
    to summarize the input code

    Input: Seq2Seq_Inference object, input code string

    Returns: predicted docstring

    """
    emb, gen_docstring = seq2seq_inf.predict(input_code)
    return gen_docstring

def summarize_dataset(code_summarizer, all_functions_path, outfile_path):
    #read in function file
    loadpath = Path(all_functions_path)
    with open(loadpath/'all_functions.function') as in_file:
      lineList = in_file.readlines()

    #create and open output file
    loadpath = Path(outfile_path)
    out_file= open(loadpath/"generated_docstrings.docstring","w+")

    #write summaries to out file
    for line in lineList:
        out_file.write(summarize_function(code_summarizer, line) + '\n')

    #close out file
    out_file.close()
