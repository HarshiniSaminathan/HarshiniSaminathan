
from app.models.dbModels import db

class User(db.Document):
    emailid = db.StringField(required=True, primary_key=True)
    password = db.StringField(required=True)
    username = db.StringField(required=True)
    fullname = db.StringField(required=True)
    role = db.StringField(required=True)
    status = db.StringField(required=True)
    accountType =db.StringField(required=True)
    created_at = db.DateTimeField(required=True)
    sessionCode = db.StringField()