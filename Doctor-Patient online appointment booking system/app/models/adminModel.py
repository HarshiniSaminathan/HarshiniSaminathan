
from app.models.userModel import db

class AdminTable(db.Model):
    __tablename__ = 'adminTable'
    adminId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    adminName = db.Column(db.String(255))
    adminPhoneNumber = db.Column(db.String(20))
    adminAddress = db.Column(db.String(255))
    emailId = db.Column(db.String(255), db.ForeignKey('userTable.emailId', ondelete='CASCADE'), unique=True)
    user = db.relationship('UserTable', back_populates='admin', uselist=False)
