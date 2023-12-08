
from app.models.dbModels import db


class Post(db.Document):
    emailid = db.StringField(required=True)
    postType = db.StringField(required=True)
    post = db.StringField(required=True)
    caption = db.StringField()
    created_at = db.DateTimeField(required=True)
    status = db.StringField(required=True)
    tagUsername = db.ListField()







