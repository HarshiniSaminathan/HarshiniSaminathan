from app.models.userModel import db

class PatientTable(db.Model):
    __tablename__ = 'patientTable'
    patientId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patientFirstName = db.Column(db.String(255))
    patientLastName = db.Column(db.String(255))
    patientPhoneNumber = db.Column(db.String(20))
    patientDOB = db.Column(db.Date)
    patientAddress = db.Column(db.String(255))
    patientEmailId = db.Column(db.String(255), db.ForeignKey('userTable.emailId', ondelete='CASCADE'), unique=True)
    user = db.relationship('UserTable', back_populates='patient', uselist=False)
