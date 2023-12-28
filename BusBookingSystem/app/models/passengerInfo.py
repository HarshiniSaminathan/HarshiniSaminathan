from app.models.dbModels import db

class PassengerDetails(db.Document):
    passenger_names = db.StringField(required=True)
    gender = db.StringField(required=True)
    age = db.StringField(required=True)
    id_proof_type = db.StringField(required=True)
    id_proof = db.StringField(required=True)
    seats = db.StringField(required=True)