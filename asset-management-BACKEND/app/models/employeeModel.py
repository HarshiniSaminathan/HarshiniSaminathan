from datetime import datetime

from app.models.dbModel import db
class EmployeeTable(db.Model):
    __tablename__ = "Employee"
    emp_pk_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_id = db.Column(db.Integer, unique=True)
    emp_name = db.Column(db.String)
    emp_status = db.Column(db.String)
    emp_emailId = db.Column(db.String)
    designation = db.Column(db.String)
    company_name = db.Column(db.String)
    AssetAssignment = db.relationship('AssetAssignmentTable', backref='employee', uselist=False)
    AccessoriesAss = db.relationship('AccessoriesAssTable', backref='employee', uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
