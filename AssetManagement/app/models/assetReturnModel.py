from app.models.dbModel import db
from sqlalchemy import func

class AssetReturnTable(db.Model):
    __tablename__ = "AssetReturnTable"
    AssetReturnId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AssetId = db.Column(db.Integer, db.ForeignKey('AssetTable.AssetId', ondelete='CASCADE'))
    EmployeeId = db.Column(db.Integer, db.ForeignKey('EmployeeTable.EmployeeId', ondelete='CASCADE'))
    AssignmentIssueDate = db.Column(db.Date)
    ReturnDate = db.Column(db.Date)
    ReturnType = db.Column(db.String(30))
    Return = db.Column(db.String(30))
    createdOn = db.Column(db.Date, server_default=func.current_date())
    createdAt = db.Column(db.Time, server_default=func.current_time())
    editedOn = db.Column(db.Date)
    editedAt = db.Column(db.Time)