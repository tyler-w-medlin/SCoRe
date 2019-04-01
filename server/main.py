"""
Main server file. It loads the necessary components and starts the server

Author: Elliott Campbell
For: US-3

Last Updated: March 31, 2019
"""

from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flask import Flask, jsonify, request

from flask_cors import CORS

import json
import os
import sys
sys.path.append('./tools')
sys.path.append('../data/lang_model')

import searchInit

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# ==========================================================================================================
# Initialize Flask SQLAlchemy binders and database - Elliott Campbell
# ==========================================================================================================

# print("sqlite:////" + os.path.join(basedir, "database", "sources.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.path.join(basedir, "database", "score.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ==========================================================================================================
# Initialize Search engine - Elliott Campbell
# ==========================================================================================================

engine = searchInit.searchEngineInit()


# ==========================================================================================================
# Database Table schema for our information and files
# ==========================================================================================================
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw_code = db.Column(db.Text, unique=True, nullable=False)
    vector_coordinates = db.Column(db.LargeBinary)
    docstring = db.Column(db.Text)
    keywords = db.Column(db.Text)

    def to_dict(self):
        """
        Returns a dictionary representation of the database model object
        """

        return {
            "id": self.id,
            "raw_code": self.raw_code,
            "docstring": self.docstring,
            "coordinates": self.vector_coordinates,
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
    # ==========================================================================================================
    results = engine.search(posted["search"])

    # queries = set()
    # for word in keywords:
    #     for query in Score.query.filter(Score.keywords.contains(word)).all():
    #         queries.add(query)

    # results = {}
    # for i in range(len(queries)):
    #     results[str(i)] = queries.pop().to_dict()

    return jsonify(results)


# ==========================================================================================================
# Run the server on the appropriate 0.0.0.0 IP address
# ==========================================================================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0")
