from app.models.userModel import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
class PatientTable(db.Model):
    __tablename__ = 'patientTable'
    patientId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patientFirstName = db.Column(db.String(255))
    patientLastName = db.Column(db.String(255))
    patientPhoneNumber = db.Column(db.String(20))
    patientDOB = db.Column(db.Date)
    patientAddress = db.Column(db.String(255))
    patientEmailId = db.Column(db.String(255), db.ForeignKey('userTable.emailId', ondelete='CASCADE'), unique=True)
    user = relationship('UserTable', back_populates='patient', uselist=False) #removed.db
    appointments = db.relationship("appointmentTable", back_populates="patient")  #.db added # one-many
    feedback_sessions = db.relationship('FeedbackSession', back_populates='patient')
