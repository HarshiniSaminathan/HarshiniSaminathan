from app.models.userModel import db


class slotTable(db.Model):
    __tablename__ = 'slotTable'
    slotId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctorId = db.Column(db.Integer, db.ForeignKey('doctorTable.doctorId', ondelete='CASCADE'))
    slotStatus = db.Column(db.Boolean)
    slotStartTime = db.Column(db.Time)
    slotEndTime = db.Column(db.Time)
    doctor = db.relationship('DoctorTable', back_populates='slots') #added


