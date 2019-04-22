"""
Main server file. It loads the necessary components and starts the server

Author: Elliott Campbell
For: US-3

Last Updated: March 31, 2019
"""

from flask_sqlalchemy import SQLAlchemy

from flask import Flask, jsonify, request, render_template

from flask_cors import CORS
import numpy as np

import json
import os
import sys

from io import BytesIO
from zipfile import ZipFile
import re

sys.path.append('./tools')
sys.path.append('../data/lang_model')

import searchInit

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_name = "score.db"
# ==========================================================================================================
# Initialize Flask SQLAlchemy binders and database - Elliott Campbell
# ==========================================================================================================

# print("sqlite:////" + os.path.join(basedir, "database", "sources.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.path.join(basedir, "database", db_name)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


check_extension = re.compile(".py$")

# ==========================================================================================================
# Database Table schema for our information and files
# ==========================================================================================================
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw_code = db.Column(db.Text, unique=True, nullable=False)

     # Stored as bytestring for LargeBinary, so be sure to decode
    vector_coordinates = db.Column(db.LargeBinary)

    project_path = db.Column(db.Text)
    keywords = db.Column(db.Text)

    def to_dict(self):
        """
        Returns a dictionary representation of the database model object.
        NOTE: the coordinates are stored as byte string and needs to be decoded
              using np.fromstring()
        """

        return {
            "id": self.id,
            "raw_code": self.raw_code,
            "coordinates": "coordinates",
            "keywords": self.keywords
        }

    def __str__(self):
        """
        returns the expected string representation ofthe database object model
        """
        return str(self.to_dict())

    def __repr__(self):
        """
        basic representation of the database object model as an object in Python
        """
        return "<Score {}>".format(self.id)




# ==========================================================================================================
# Enable CORS allos us to not have to worry about header information being correct/incorrect or having
# a specfied IP address that is allowed to ping the server.
# ==========================================================================================================
CORS(app)

def add_to_database(info):
    item = Score(
        raw_code = info["code_snippet"],
        vector_coordinates = info["vectorization"][0].astype(np.float64).tostring(),
        project_path = None,
        keywords = info["docstring"]
    )


    db.session.add(item)
    db.session.flush()
    engine.search_index.addDataPoint(item.id - 1, info["vectorization"][0].astype(np.float64))
    db.session.commit()

def update():
    for item in Score.query.all():
#         print("""
#     id: {},
#     coords: {},
# """.format(item.id, np.fromstring(item.vector_coordinates)))
        # print(item.vector_coordinates)
        engine.search_index.addDataPoint(item.id - 1, np.fromstring(item.vector_coordinates))
    # print(np.fromstring(Score.query.get(159).vector_coordinates))
    # print(Score.query.get(158))
    engine.search_index.createIndex()

# =========================================================================================================




# ==========================================================================================================
# Initialize Search engine - Elliott Campbell
# ==========================================================================================================

engine = searchInit.searchEngineInit()
update()
    
# ==========================================================================================================
# Leftover from basic learning of the server. Can be removed, but doesn't bother anything at the moment.
# ==========================================================================================================

@app.route("/hello")
def send_hello():

    return jsonify({
        "response" : "Hello, world"
    })

# ==========================================================================================================
# The API route to send the search. As of now, the search can only be done through JSON input
# ==========================================================================================================

@app.route("/search", methods = ["POST"])
def search():
    """
    A setup for the API route in order to receive a POST request in
    applicat/json form and return the search query in application/json
    as well.
    
    @params: None
    @input: application/json in format:
                {
                    "search" <search_terms/search_string>
                }
    @output: application/json in format:
                { 
                    N (where n is the result number):
                    {
                        "keywords": <keywords from query result>,
                        "relevancy": <relevancy as defined by cosine distance>,
                        "raw_code": <original, raw code inserted into db>
                    }
                }
    """

    # ==========================================================================================================
    # Parse the received json from the POSt event
    # ==========================================================================================================
    posted = json.loads(request.data.decode())

    
    # ==========================================================================================================
    # Search for the relevant queries
    # Should receive the ID/array location of the appropriate result and the distance/releveancy of the result
    #   and the query.
    # ==========================================================================================================
    idxs, dists = engine.search(posted["search"])

    results = {}
    number = 1
    for idx, dist in zip(idxs, dists):

        query = Score.query.get(int(idx + 1))

        results[number] = {
            "keywords" : query.keywords,
            "relevancy" : "{:0.4f}".format(1 - dist),
            "raw_code" : query.raw_code
        }

        number += 1


    return jsonify(results)

@app.route("/addCode", methods = ["POST"])
def add():
    """
    TODO: Currently, the on the fly embeddings don't work well. They produce low space 0 vectors and creates
          an issue when creating the database at initialization.
    """
    try:
        posted = json.loads(request.data.decode())

        if "docstring" in posted:
            things_to_add = engine.prep_code(posted["code"], posted["docstring"])
        else:
            things_to_add = engine.prep_code(posted["code"])

    except:
        try:
            data = BytesIO(request.data).getvalue().decode()
            things_to_add = engine.prep_code(data, file=True)
            for info in things_to_add:
                add_to_database(info)
        except:
            data = BytesIO(request.data)
            with ZipFile(data) as zip:
                files = [file for file in zip.filelist if check_extension.search(file.filename)]

                for file in files:
                    with zip.open(file) as f:
                        code = f.read().decode()
                    things_to_add = engine.prep_code(code, file=True)
                    for info in things_to_add:
                        add_to_database(info)

    engine.search_index.createIndex()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


# ==========================================================================================================
# Server route/function definitions
# ==========================================================================================================
@app.route("/", defaults={"path": ''})
@app.route("/<path:path>")
def send_index(path):
    return render_template("score.html")



# ==========================================================================================================
# Run the server on the appropriate 0.0.0.0 IP address
# ==========================================================================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
