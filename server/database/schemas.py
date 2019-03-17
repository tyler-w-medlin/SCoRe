from main import db
# class Project(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True, nullable=False)
#     Details = db.Column(db.String)

# class FunctionalRequirement(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String)
#     parent_id = db.Column(db.Integer)
#     tag = db.Column(db.String)
    
#     project_id = db.Column(db.Integer, db.ForeignKey("project.id"),
#         nullable=False)
#     project = db.relationship("Project", backref=db.backref("functionalrequirements", lazy=True))

#     file_name = db.Column(db.String, db.ForeignKey("files.file_name"), nullable=False)
#     files = db.relationship("ProjectFile", backref=db.backref("functionalrequirements", lazy=True))


# class NonFunctionalRequirement(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String)
#     parent_id = db.Column(db.Integer)
#     tag = db.Column(db.String)
    
#     project_id = db.Column(db.Integer, db.ForeignKey("project.id"),
#                            nullable=False)
#     project = db.relationship("Project", backref=db.backref(
#         "nonfunctionalrequirements", lazy=True))
    
#     functional_req_id = db.Column(db.Integer, db.ForeignKey("FR.id"))
#     FR = db.relationship("FunctionalRequirement", backref=db.backref(
#         "nonfunctionalrequirements", lazy=True))
    
#     file_name = db.Column(db.String, db.ForeignKey(
#         "files.file_name"), nullable=False)
#     files = db.relationship("ProjectFile", backref=db.backref(
#         "nonfunctionalrequirements", lazy=True))


# class ProjectFile(db.Model):
#     file_name = db.Column(db.String, primary_key=True)
#     functiona_name = db.Column(db.String)
#     line_start = db.Column(db.Integer)
#     line_end = db.Column(db.Integer)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    raw_code = db.Column(db.Text, unique = True, nullable = False)
    vector_coordinates = db.Column(db.Float)
    keywords = db.Column(db.Text)

    def to_dict(self):
        
        return {
            "id" : self.id,
            "raw_code" : self.raw_code,
            "coordinates": self.vector_coordinates,
            "keywords" : self.keywords
        }
    
    def __repr__(self):
        return self.to_dict()