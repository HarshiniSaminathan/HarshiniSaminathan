from app.models.dbModel import db
from sqlalchemy import func

class AssetAssignmentTable(db.Model):
    __tablename__ = "AssetAssignmentTable"
    AssetAssignmentId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AssetId = db.Column(db.Integer, db.ForeignKey('AssetTable.AssetId', ondelete='CASCADE'))
    EmployeeId = db.Column(db.Integer, db.ForeignKey('EmployeeTable.EmployeeId', ondelete='CASCADE'))
    AssignmentIssueDate = db.Column(db.Date)
    createdOn = db.Column(db.Date, server_default=func.current_date())
    createdAt = db.Column(db.Time, server_default=func.current_time())
    editedOn = db.Column(db.Date)
    editedAt = db.Column(db.Time)
