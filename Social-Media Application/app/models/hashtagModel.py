
from app.models.dbModels import db

class Hashtag(db.Document):
    hashtag = db.StringField(required=True)
    postid = db.ListField(required=True)
    created_at = db.DateTimeField(required=True)
