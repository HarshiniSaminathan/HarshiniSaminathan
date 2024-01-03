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
    doctor = db.relationship("DoctorTable", back_populates="appointments") # db.
    patient = db.relationship("PatientTable", back_populates="appointments") #db.
    medical_record = db.relationship("MedicalRecordsTable", back_populates="appointment") # line
    prescription = db.relationship("PrescriptionTable", back_populates="appointment")  # line
    pmr_record = db.relationship("PMRecordTable", back_populates="appointment")  # line

