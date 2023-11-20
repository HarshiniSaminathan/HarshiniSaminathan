from app.models.userModel import db


class slotTable(db.Model):
    __tablename__ = 'slotTable'
    slotId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctorId = db.Column(db.Integer, db.ForeignKey('doctorTable.doctorId', ondelete='CASCADE'))
    slotStatus = db.Column(db.String(255))
    slotDateTime = db.Column(db.DateTime)


