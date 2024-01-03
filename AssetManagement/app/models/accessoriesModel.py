from app.models.dbModel import db
from sqlalchemy import func

class AccessoriesTable(db.Model):
    __tablename__ = "AccessoriesTable"
    AccessoriesId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EmployeeId = db.Column(db.Integer, db.ForeignKey('EmployeeTable.EmployeeId', ondelete='CASCADE'))
    AccessoriesIssueDate = db.Column(db.Date)
    ReturnDate = db.Column(db.Date)
    ReturnType = db.Column(db.String(30))
    ReturnCondition = db.Column(db.String(30))
    createdOn = db.Column(db.Date, server_default=func.current_date())
    createdAt = db.Column(db.Time, server_default=func.current_time())
    editedOn = db.Column(db.Date)
    editedAt = db.Column(db.Time)