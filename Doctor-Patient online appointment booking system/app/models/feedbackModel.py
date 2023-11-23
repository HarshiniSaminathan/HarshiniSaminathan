from app.models.userModel import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.patientModel import PatientTable
from sqlalchemy import Time

class FeedbackSession(db.Model):
    __tablename__ = 'FeedbackSession'
    feedbackSessionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctorId = db.Column(db.Integer, db.ForeignKey('doctorTable.doctorId',ondelete='CASCADE'))
    patientId = db.Column(db.Integer, db.ForeignKey('patientTable.patientId',ondelete='CASCADE'))

    doctor = db.relationship("DoctorTable", back_populates='feedback_sessions')
    patient = db.relationship("PatientTable", back_populates='feedback_sessions')

    feedbackTextForAdmin = db.Column(db.Text)
    feedbackTextForDoctor = db.Column(db.Text)
    feedbackResponse = db.Column(db.Text)
    rating = db.Column(db.Integer)
    createdDate = db.Column(db.Date)
    createdTime = db.Column(db.Time)







