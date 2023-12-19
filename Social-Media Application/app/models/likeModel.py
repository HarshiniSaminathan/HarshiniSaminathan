
from app.models.dbModels import db


class Like(db.Document):
    postid = db.StringField(required=True)
    emailid = db.StringField(required=True)
    created_at = db.DateTimeField(required=True)
