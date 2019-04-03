# ==============================================================
# This file is mostly for accessing and populating that database
# It should not be run for any other purpose. It's basically just
# a scratch file.
# ==============================================================

import numpy as np
from main import db, Score, engine

# tests = [
#     Score(
#         raw_code = """
# def foo():
#     return bar
# """,
#         vector_coordinates = None,
#         keywords = "foo bar"
#     ),
#     Score(
#         raw_code = """"
# def bar():
#     return foo
# """,
#         vector_coordinates = None,
#         keywords = "bar foo"
#     )
# ]
vector_embeds = np.load('tools/data/lang_model_emb/dataset_embedding.npy')

for i in range(len(engine.function_data)):
    # print(engine.docstring_data[i])
    # print(engine.function_data[i])
    # print(vector_embeds[0])
    
    print(Score.query.get(i))



