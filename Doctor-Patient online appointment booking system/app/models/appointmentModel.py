from app.models.userModel import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class appointmentTable(db.Model):
    __tablename__ = 'appointmentTable'
    appointmentId = db.Column(db.Integer, primary_key=True,autoincrement=True)
    doctorId =db.Column(db.Integer,db.ForeignKey('doctorTable.doctorId', ondelete='CASCADE'))
    patientId=db.Column(db.Integer,db.ForeignKey('patientTable.patientId',ondelete='CASCADE'))
    appointmentStatus=db.Column(db.String(255))
    appointmentDate = db.Column(db.Date)
    appointmentTime =db.Column(db.Time)
    doctor = relationship("DoctorTable", back_populates="appointments")
    patient = relationship("PatientTable", back_populates="appointments")



