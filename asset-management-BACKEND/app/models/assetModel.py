from datetime import datetime
from app.models.dbModel import db


class AssetTable(db.Model):
    __tablename__ = "Asset"
    asset_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    asset_Serial_no = db.Column(db.Integer, unique=True)
    asset_type = db.Column(db.String)
    asset_name = db.Column(db.String)
    asset_os = db.Column(db.String)
    asset_spec = db.Column(db.String)
    asset_price = db.Column(db.String)
    asset_validity = db.Column(db.String)
    issued_at = db.Column(db.Date)
    asset_status = db.Column(db.String)
    vendor_id = db.Column(db.Integer, db.ForeignKey('Vendor.vendor_id', ondelete='CASCADE'))
    vendor_assets = db.relationship('VendorTable', backref='asset_vendors')
    AssetAssignment = db.relationship('AssetAssignmentTable', backref='asset', uselist=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
