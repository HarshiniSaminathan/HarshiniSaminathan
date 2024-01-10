from datetime import datetime
from app.models.dbModel import db


class VendorTable(db.Model):
    __tablename__ = "Vendor"
    vendor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_name = db.Column(db.String, unique=True)
    vendor_status = db.Column(db.String)
    location = db.Column(db.String)
    Asset = db.relationship('AssetTable', backref='Asset', uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
