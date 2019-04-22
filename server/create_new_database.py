from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

def ask_name():
    return input("Enter name of database ('database' or 'score'): ")

def create_file(file_name):
    with open("database/{}.db".format(file_name), "w") as f:
        pass
    

if __name__ == "__main__":
    file_name = ask_name()
    create_file(file_name)


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.path.join(basedir, "database", "{}.db".format(file_name))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

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


db.create_all()

print("Your database has been created. In main.py change the db_name variable to {}.db".format(file_name))