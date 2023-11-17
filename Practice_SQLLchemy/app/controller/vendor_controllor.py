
from app.models.user_model import db,Vendor
from app.utils.comman_utils import add_in_entity, update_in_entity, delete_in_entity


def check_vendor_email_existence(vendoremailid):
    count = Vendor.query.filter_by(vendoremailid=vendoremailid).count()
    if count > 0:
        return True
    else:
        return False

def insert_vendor(vendoremailid, vendorname, mobileno, address):
    new_vendor = Vendor(
        vendoremailid=vendoremailid,
        vendorname=vendorname,
        mobileno=mobileno,
        address=address
    )
    add_in_entity(new_vendor)


def fetch_vendor_data():
    vendors=Vendor.query.all()
    data=[]
    for vendor in vendors:
        data.append(
                {
                    "vendoremailid": vendor.vendoremailid,
                    "vendorname": vendor.vendorname,
                    "mobileno": vendor.mobileno,
                    "address": vendor.address
                })
    return data

def get_total_records():
    total_records = Vendor.query.count()
    return total_records

def update_vendor(vendoremailid,vendorname,mobileno,address):
    try:
        vendor= Vendor.query.filter_by(vendoremailid=vendoremailid).first()
        if vendor:
            vendor.vendoremailid=vendoremailid
            vendor.vendorname=vendorname
            vendor.mobileno=mobileno
            vendor.address=address
            update_in_entity()
            return True
        else:
            return False
    except Exception as e:
        return False

def delete_vendor(vendoremailid):
    vendor =Vendor.query.filter_by(vendoremailid=vendoremailid).first()
    if vendor:
        delete_in_entity(vendor)
        return True
    else:
        return False

def list_vendor_names():
    vendors = Vendor.query.with_entities(Vendor.vendorname).all()
    vendor_names = [vendor.vendorname for vendor in vendors]
    return vendor_names


