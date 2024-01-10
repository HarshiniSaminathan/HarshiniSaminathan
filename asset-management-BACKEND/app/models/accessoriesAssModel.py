from app.models.dbModel import db
from datetime import datetime

class AccessoriesAssTable(db.Model):
    __tablename__ = "AccessoriesAssignment"
    acc_assign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_pk_id = db.Column(db.Integer, db.ForeignKey('Employee.emp_pk_id', ondelete='CASCADE'))
    accessory_id = db.Column(db.Integer, db.ForeignKey('Accessories.accessory_id', ondelete='CASCADE'))
    assigned_at = db.Column(db.Date)
    return_at = db.Column(db.Date)
    return_type = db.Column(db.String)
    condition = db.Column(db.String)
    employee_ass = db.relationship('EmployeeTable', backref='Emp_assignment')
    Ass_Accessories = db.relationship('AccessoriesTable', backref='accessories_assignment')
