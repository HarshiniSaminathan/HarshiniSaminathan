from app.models.userModel import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class MedicalRecordsTable(db.Model):
    __tablename__ = 'MedicalRecordsTable'
    medicalRecordId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255))
    PMReport = db.Column(db.LargeBinary)
    appointmentId = db.Column(db.Integer, db.ForeignKey('appointmentTable.appointmentId', ondelete='CASCADE'))
    appointment = db.relationship("appointmentTable", back_populates="medical_record") #line
    createdDate = db.Column(db.Date)
    createdTime = db.Column(db.Time)


