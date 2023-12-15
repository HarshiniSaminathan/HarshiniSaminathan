from app.models.userModel import db


class CommerceCSVModel(db.Model):
    __tablename__ = 'CommerceCSVModel'
    ID = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String)
    SKU = db.Column(db.String)
    Name = db.Column(db.String)
    Published = db.Column(db.String)
    featured = db.Column(db.String)
    Visibilityincatalog = db.Column(db.String)
    Shortdescription = db.Column(db.String)




