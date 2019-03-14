from code_summarizer import load_Summarizer, summarize
import pandas as pd

input_code = "def db_connect self try global conn conn sqlite3 connect database database db except print An error was encountered while trying to connect to the database global curr curr conn cursor"
input_docstring = "Connected to database"

#load the summarizer model
seq2seq_obj = load_Summarizer()


print(f"\n****** Input Code ******\n {input_code}")
print(f"\n****** Original Docstring ******\n {input_docstring}")
#print the predicted docstring
print(f"\n****** Predicted Docstring ******\n {summarize(seq2seq_obj, input_code)}\n")
