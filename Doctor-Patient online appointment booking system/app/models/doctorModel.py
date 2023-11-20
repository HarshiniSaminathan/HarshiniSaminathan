from app.models.userModel import db

class DoctorTable(db.Model):
    __tablename__ = 'doctorTable'
    doctorId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctorName = db.Column(db.String(255))
    doctorPhoneNumber = db.Column(db.String(20))
    doctorAddress = db.Column(db.String(255))
    doctorExperience = db.Column(db.String(255))
    doctorSpecialization = db.Column(db.String(255))
    doctorSpecializationProof = db.Column(db.LargeBinary)
    doctorEmailId = db.Column(db.String(255), db.ForeignKey('userTable.emailId', ondelete='CASCADE'), unique=True)
    user = db.relationship('UserTable', back_populates='doctor', foreign_keys=[doctorEmailId])
