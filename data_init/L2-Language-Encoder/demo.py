import sys
sys.path.append('../language_encoder')
from l2_language_encoder import load_code2emb, code2emb
from language_encoder import load_encoder, encode

input_code = "def db_connect self try global conn conn sqlite3 connect database database db except print An error was encountered while trying to connect to the database global curr curr conn cursor"

input_string = "connect to database"

LANG_MODEL_PATH = '../data/lang_model'
CODE2EMB_PATH = '../data/code2emb/code2emb_model.hdf5'
SEQ2SEQ_PATH = '../data/seq2seq/py_code_proc_v2.dpkl'

c2e_model, pp = load_code2emb(CODE2EMB_PATH, SEQ2SEQ_PATH)

lang_encoder = load_encoder(LANG_MODEL_PATH, LANG_MODEL_PATH)

c2e = code2emb(input_code, c2e_model, pp)

str2e = encode(lang_encoder, input_string)

print(c2e)

print(str2e)

assert c2e.shape[0] == str2e.shape[0]
