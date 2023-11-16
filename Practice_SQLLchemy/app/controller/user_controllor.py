from datetime import datetime

from app.models.user_model import db,User

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
    db.session.add(new_user)
    db.session.commit()

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
            db.session.commit()
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
        db.session.delete(user)
        db.session.commit()
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
