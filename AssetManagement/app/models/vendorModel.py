from app.models.dbModel import db
from sqlalchemy import func
class VendorTable(db.Model):
    __tablename__ = "VendorTable"
    VendorId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    VendorName = db.Column(db.String(30), unique=True)
    Asset = db.relationship('AssetTable', backref='Asset', uselist=False)
    createdOn = db.Column(db.Date, server_default=func.current_date())
    createdAt = db.Column(db.Time, server_default=func.current_time())
    editedOn = db.Column(db.Date)
    editedAt = db.Column(db.Time)