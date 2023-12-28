from app.models.userModel import User
from app.models.passengerInfo import PassengerDetails
import datetime
from datetime import datetime, timedelta
def check_email_existence(emailid):
    return User.objects(emailid=emailid).first() is not None

import hashlib

def hash_password(password):
   password_bytes = password.encode('utf-8')
   hash_object = hashlib.sha256(password_bytes)
   return hash_object.hexdigest()

def insert_user(emailid, password, fullname, role):
    current_datetime = datetime.utcnow().isoformat()
    user = User(
        emailid=emailid,
        hashedpassword=hash_password(password),
        fullname=fullname,
        role=role,
        created_at=current_datetime
    )
    user.save()

def save_passenger(seats_selection,passenger_names,gender,age,id_proof_type,id_proof):
    passenger_details = PassengerDetails(
            passenger_names=passenger_names,
            gender=gender,
            age=age,
            id_proof_type=id_proof_type,
            id_proof=id_proof,
            seats=seats_selection
        )
    passenger_details.save()
    return passenger_details
