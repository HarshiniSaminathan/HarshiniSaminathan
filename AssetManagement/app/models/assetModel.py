from app.models.dbModel import db
from sqlalchemy import func

class AssetTable(db.Model):
    __tablename__ = "AssetTable"
    AssetId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AssetSerialNumber = db.Column(db.Integer, unique=True)
    AssetType = db.Column(db.String(30))
    AssetName = db.Column(db.String(30))
    Os = db.Column(db.String(10))
    AssetSpecification = db.Column(db.String(255))
    AssetPrice = db.Column(db.String(255))
    AssetValidity = db.Column(db.String(20))
    AssetIssueDate = db.Column(db.Date)
    VendorId = db.Column(db.Integer, db.ForeignKey('VendorTable.VendorId', ondelete='CASCADE'))
    AssetAssignment = db.relationship('AssetAssignmentTable', backref='Assignment', uselist=False)
    AssetReturn = db.relationship('AssetReturnTable', backref='AssetReturn', uselist=False)
    createdOn = db.Column(db.Date, server_default=func.current_date())
    createdAt = db.Column(db.Time, server_default=func.current_time())
    editedOn = db.Column(db.Date)
    editedAt = db.Column(db.Time)