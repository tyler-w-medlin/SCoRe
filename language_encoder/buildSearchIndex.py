"""
This program build the search index for the langauge encoder
REQUIRED:
    - docstring embeddings
    - to follow the baseline download the embedding from: https://storage.googleapis.com/kubeflow-examples/code_search/data/lang_model_emb/avg_emb_dim500_test_v2.npy
      then place that file in the '/data/lang_model_emb/' directory
"""
from general_utils import create_nmslib_search_index
import nmslib
from pathlib import Path
import numpy as np

# Load matrix of vectors
loadpath = Path('../data/lang_model_emb/')
avg_emb_dim500 = np.load(loadpath/'avg_emb_dim500_test_v2.npy') #docstring embeddings

# Build search index 
# (takes about an hour on a p3.8xlarge) 
# ^ that is a dirty lie. You can do it. Just believe.
dim500_avg_searchindex = create_nmslib_search_index(avg_emb_dim500)

# Save search index
dim500_avg_searchindex.saveIndex('../data/lang_model_emb/new_dim500_avg_searchindex.nmslib')