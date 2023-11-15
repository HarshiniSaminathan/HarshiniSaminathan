

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'userinfo'
    emailid = db.Column(db.String(255), primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    mobileno = db.Column(db.String(15))
    dob = db.Column(db.Date)
    address = db.Column(db.String(255))
    recenttime = db.Column(db.DateTime)
