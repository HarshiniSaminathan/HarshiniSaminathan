from app.models.dbModels import db

class BusInfo(db.Document):
    busNumber = db.StringField(required=True)
    capacity = db.StringField(required=True)
    routeFrom = db.StringField(required=True)
    routeTo = db.StringField(required=True)
    arriveTime = db.StringField(required=True)
    departureTime = db.StringField(required=True)
    status = db.StringField(required=True)
    created_at = db.DateTimeField(required=True)
    amount = db.StringField(required=True) # added