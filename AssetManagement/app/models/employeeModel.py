from app.models.dbModel import db
from sqlalchemy import func
class EmployeeTable(db.Model):
    __tablename__ = "EmployeeTable"
    EmployeeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EmployeeNumber = db.Column(db.Integer, unique=True)
    EmployeeName = db.Column(db.String(30))
    Assignment = db.relationship('AssetAssignmentTable', backref='AssetAssignment', uselist=False)
    AssetReturn = db.relationship('AssetReturnTable', backref='AssetReturn', uselist=False)
    Accessories = db.relationship('AccessoriesTable', backref='AccessoriesTable', uselist=False)
    createdOn = db.Column(db.Date, server_default=func.current_date())
    createdAt = db.Column(db.Time, server_default=func.current_time())
    editedOn = db.Column(db.Date)
    editedAt = db.Column(db.Time)