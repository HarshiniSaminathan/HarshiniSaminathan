from app.models.dbModels import db

class User(db.Document):
    emailid = db.StringField(required=True, primary_key=True)
    hashedpassword = db.StringField(required=True)
    fullname = db.StringField(required=True)
    role = db.StringField(required=True)
    created_at = db.DateTimeField(required=True)
    sessionCode = db.StringField()