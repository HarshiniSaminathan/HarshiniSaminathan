from app.models.userModel import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class PrescriptionTable(db.Model):
    __tablename__ = 'PrescriptionTable'
    PrescriptionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    medication = db.Column(db.String(255))
    dosage = db.Column(db.String(255))
    instruction = db.Column(db.String(255))
    appointmentId = db.Column(db.Integer, db.ForeignKey('appointmentTable.appointmentId', ondelete='CASCADE'))
    appointment = db.relationship("appointmentTable", back_populates="prescription") #line
    createdDate = db.Column(db.Date)
    createdTime = db.Column(db.Time)

