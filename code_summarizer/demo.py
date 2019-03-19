from code_summarizer import load_summarizer, summarize_function, summarize_dataset

PROCESSED_DATA_PATH = '../data/processed_data'
SEQ2SEQ_PATH = '../data/seq2seq'

input_code = "def db_connect self try global conn conn sqlite3 connect database database db except print An error was encountered while trying to connect to the database global curr curr conn cursor"
input_docstring = "Connected to database"

#load the summarizer model
code_summarizer = load_summarizer(SEQ2SEQ_PATH, SEQ2SEQ_PATH)


print(f"\n****** Input Code ******\n {input_code}")
print(f"\n****** Original Docstring ******\n {input_docstring}")
#print the predicted docstring
print(f"\n****** Predicted Docstring ******\n {summarize_function(code_summarizer, input_code)}\n")

summarize_dataset(code_summarizer, PROCESSED_DATA_PATH, PROCESSED_DATA_PATH)
