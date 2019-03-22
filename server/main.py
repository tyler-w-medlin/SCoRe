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


# ---------------------------------------------
# Initialize Search engine
# - written by: Elliott
# ---------------------------------------------

engine = searchInit.searchEngineInit()

# ---------------------------------------------
# Server crap - Elliott
# ---------------------------------------------
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# print("sqlite:////" + os.path.join(basedir, "database", "sources.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.path.join(basedir, "database", "score.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw_code = db.Column(db.Text, unique=True, nullable=False)
    vector_coordinates = db.Column(db.Float)
    keywords = db.Column(db.Text)

    def to_dict(self):

        return {
            "id": self.id,
            "raw_code": self.raw_code,
            "coordinates": self.vector_coordinates,
            "keywords": self.keywords
        }

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return "<Score {}>".format(self.id)

CORS(app)

@app.route("/hello")
def send_hello():

    return jsonify({
        "response" : "Hello, world"
    })

@app.route("/search", methods = ["POST"])
def search():
    posted = json.loads(request.data.decode())

    results = engine.search(posted["search"])

    # queries = set()
    # for word in keywords:
    #     for query in Score.query.filter(Score.keywords.contains(word)).all():
    #         queries.add(query)

    # results = {}
    # for i in range(len(queries)):
    #     results[str(i)] = queries.pop().to_dict()

    return jsonify(results)



if __name__ == "__main__":
    app.run(host="0.0.0.0")
