from app.models.dbModel import db
from datetime import datetime


class AccessoriesTable(db.Model):
    __tablename__ = "Accessories"
    accessory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    accessory_name = db.Column(db.String,unique=True)
    accessory_count = db.Column(db.Integer)
    assigned_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    Accessory_ass = db.relationship('AccessoriesAssTable', backref='AccessoriesAss', uselist=False)
