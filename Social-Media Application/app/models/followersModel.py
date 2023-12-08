
from app.models.dbModels import db


class Followers(db.Document):
    emailid = db.StringField(required=True)
    followerEmailid = db.StringField(reqired=True)
    status = db.StringField(required=True)
    request_at = db.DateTimeField(required=True)






