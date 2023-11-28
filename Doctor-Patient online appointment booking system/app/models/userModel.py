from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class UserTable(db.Model):
    __tablename__ = 'userTable'
    emailId = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(10))
    sessionCode = db.Column(db.String(255))
    admin = db.relationship('AdminTable', back_populates='user', uselist=False) #one-one relationship
    doctor = db.relationship('DoctorTable', back_populates='user', uselist=False)
    patient = db.relationship('PatientTable', back_populates='user', uselist=False)

# class UserTable(db.Model):
#     __tablename__ = 'user_Table'
#     emailId = db.Column(db.String(255), primary_key=True)
#     password = db.Column(db.String(255))
#     role = db.Column(db.String(10))
#     sessionCode = db.Column(db.String(255))
#     admin = db.relationship('AdminTable', back_populates='user', uselist=False) #one-one relationship
#     doctor = db.relationship('DoctorTable', back_populates='user', uselist=False)
#     patient = db.relationship('PatientTable', back_populates='user', uselist=False)