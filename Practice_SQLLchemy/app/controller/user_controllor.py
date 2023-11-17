from datetime import datetime

from app.models.user_model import db,User,Vendor
from app.utils.comman_utils import add_in_entity, update_in_entity, delete_in_entity


def insert_user(emailid, firstname, lastname, mobileno, dob, address):
    new_user = User(
        emailid=emailid,
        firstname=firstname,
        lastname=lastname,
        mobileno=mobileno,
        dob=dob,
        address=address,
        recenttime=datetime.now()
    )
    add_in_entity(new_user)

def check_email_existence(emailid):
    count = User.query.filter_by(emailid=emailid).count()
    if count > 0:
        return True
    else:
        return False

def update_user(emailid, firstname, lastname, mobileno, dob, address):
    try:
        user = User.query.filter_by(emailid=emailid).first()
        if user:
            user.firstname = firstname
            user.lastname = lastname
            user.mobileno = mobileno
            user.dob = dob
            user.address = address
            user.recenttime = db.func.current_timestamp()
            update_in_entity()
            return True
        else:
            return False
    except Exception as e:
        return False

def get_user_by_email(emailid):
    user = User.query.filter_by(emailid=emailid).first()
    if user:
        data = {
            'emailid': user.emailid,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'mobileno': user.mobileno,
            'dob': user.dob,
            'address': user.address,
            'recenttime': user.recenttime
        }
    return data

def delete_user(emailid):
    user = User.query.filter_by(emailid=emailid).first()
    if user:
        delete_in_entity(user)
        return True
    else:
        return False


def fetch_user_data(items_per_page, offset):
    users = User.query.order_by(User.recenttime.desc()).limit(items_per_page).offset(offset).all()
    data = []
    for user in users:
        data.append({
            'emailid': user.emailid,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'mobileno': user.mobileno,
            'dob': user.dob,
            'address': user.address,
            'recenttime': user.recenttime
        })
    return data

def get_total_records():
    total_records = User.query.count()
    return total_records

def common_email_present(emailid):
    count = User.query.filter_by(emailid=emailid).count()
    count1= Vendor.query.filter_by(vendoremailid=emailid).count()
    if count>0 or count1>0:
        return True
    else:
        return False

def common_email_count(emailid):
    useremail = User.query.filter_by(emailid=emailid).count()
    vendoremail= Vendor.query.filter_by(vendoremailid=emailid).count()
    if useremail > 0:
        return True
    if vendoremail >0:
        return False

def data_from_common_email(emailid):
    if common_email_count(emailid):
        user = User.query.get(emailid)
        result = {
            'user': {
                'emailid': user.emailid,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'mobileno': user.mobileno,
                'dob': user.dob.strftime('%Y-%m-%d') if user.dob else None,
                'address': user.address,
                'recenttime': user.recenttime.strftime('%Y-%m-%d %H:%M:%S') if user.recenttime else None
            }
        }
        return result
    elif not common_email_count(emailid):
        vendor = Vendor.query.get(emailid)
        result = {
            'vendor': {
                'vendoremailid': vendor.vendoremailid,
                'vendorname': vendor.vendorname,
                'mobileno': vendor.mobileno,
                'address': vendor.address
            }
        }
        return result