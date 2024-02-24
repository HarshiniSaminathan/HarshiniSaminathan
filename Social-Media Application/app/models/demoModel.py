from app.models.dbModels import db


class Demo(db.Document):
    emailId = db.StringField(required=True)
    name = db.StringField(required=True)
    created_at = db.DateTimeField(required=True)
    updated_at = db.DateTimeField(required=True)

