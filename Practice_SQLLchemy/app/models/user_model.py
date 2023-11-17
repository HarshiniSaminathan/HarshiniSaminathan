
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User_Table'
    emailid = db.Column(db.String(255), primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    mobileno = db.Column(db.String(15))
    dob = db.Column(db.Date)
    address = db.Column(db.String(255))
    recenttime = db.Column(db.DateTime)

class Vendor(db.Model):
    __tablename__ = 'Vendor_Table'
    vendoremailid = db.Column(db.String(255), primary_key=True)
    vendorname = db.Column(db.String(100), unique=True)
    mobileno = db.Column(db.String(15))
    address = db.Column(db.String(255))
    assets = db.relationship('Asset', backref='vendor', lazy=True)

class Asset(db.Model):
    __tablename__ = 'Asset_Table'
    AssetSerialNumber=db.Column(db.Integer,primary_key=True)
    AssetName = db.Column(db.String(255))
    AssetType = db.Column(db.String(100))
    vendorname = db.Column(db.String(100), db.ForeignKey('Vendor_Table.vendorname'))





