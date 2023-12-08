
from app.models.dbModels import db


class UserProfile(db.Document):
    emailid = db.StringField(required=True, primary_key=True)
    profileImage = db.StringField(required=True)
    profileName = db.StringField(required=True)
    bio = db.StringField(required=True)
