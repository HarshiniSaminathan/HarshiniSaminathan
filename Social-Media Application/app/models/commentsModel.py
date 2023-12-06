
from app.models.dbModels import db

class Comments(db.Document):
    postid = db.StringField(required=True)
    emailid = db.StringField(required=True)
    created_at = db.DateTimeField(required=True)
    comments = db.StringField(required=True)
    replyComment = db.ListField()









