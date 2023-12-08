
from app.models.dbModels import db

class Message(db.Document):
    senderEmailid = db.StringField(required=True)
    receiverEmailid = db.StringField(required=True)
    created_at = db.DateTimeField(required=True)
    content = db.StringField(required=True)
    read = db.BooleanField(required=True)
