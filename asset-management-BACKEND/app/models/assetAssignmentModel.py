from datetime import datetime
from app.models.dbModel import db


class AssetAssignmentTable(db.Model):
    __tablename__ = "AssetAssignment"
    assign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('Asset.asset_id', ondelete='CASCADE'))
    emp_pk_id = db.Column(db.Integer, db.ForeignKey('Employee.emp_pk_id', ondelete='CASCADE'))
    assigned_at = db.Column(db.Date)
    Returned_at = db.Column(db.Date)
    Return_type = db.Column(db.String)
    condition = db.Column(db.String)
    employee_ass = db.relationship('EmployeeTable', backref='Asset_Assignment')
    assign_Asset = db.relationship('AssetTable',backref='asset_assignment')