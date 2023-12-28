from app.models.dbModels import db
from mongoengine.fields import StringField, ListField, DateTimeField, ObjectIdField

class Bookings(db.Document):
    busId = db.ObjectIdField(required=True)
    userId = db.StringField(required=True)
    passengerDetailsIds = ListField(ObjectIdField())
    contactNumber = db.StringField(required=True)
    TotalAmount = db.StringField(required=True)
    bookingDate = db.DateField(required=True)
    status = db.StringField(required=True)
    created_at = db.DateTimeField(required=True)

    # passenger_details = db.DictField(ReferenceField(PassengerDetails), required=True)
    # seatsSelection = db.ListField(required=True)
    # passengerNames = db.ListField(required=True)
    # gender = db.ListField(required=True)
    # age = db.ListField(required=True)
    # IdProofTYpe = db.ListField(required=True)
    # IdProof = db.ListField(required=True)






