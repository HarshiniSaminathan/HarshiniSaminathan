from app.models.bookings import Bookings
from app.models.busInfoModel import BusInfo
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

def Travelled_Bookings(emailid):
    current_datetime = datetime.utcnow().isoformat()
    bookings = Bookings.objects(userId=emailid, bookingDate__lt=current_datetime).all()

    print(bookings)
    travelled_bookings = []

    for booking in bookings:
        bus_info = BusInfo.objects(id=booking.busId).first()

        if bus_info:
            bus_details = {
                'busNumber': bus_info.busNumber,
                'routeFrom': bus_info.routeFrom,
                'routeTo': bus_info.routeTo,
                'arriveTime': bus_info.arriveTime,
                'departureTime': bus_info.departureTime,
            }
            booking_details = {
                'TotalAmount': booking.TotalAmount,
                'no_of_passengers_booked': len(booking.passengerDetailsIds),
                'bookingDate': booking.bookingDate,
            }
            travelled_booking = {**bus_details, **booking_details}
            travelled_bookings.append(travelled_booking)

    return travelled_bookings

def Upcoming_Bookings(emailid):
    current_datetime = datetime.utcnow().isoformat()
    bookings = Bookings.objects(userId=emailid, bookingDate__gt=current_datetime).all()

    travelled_bookings = []
    for booking in bookings:
        bus_info = BusInfo.objects(id=booking.busId).first()

        if bus_info:
            bus_details = {
                'busNumber': bus_info.busNumber,
                'routeFrom': bus_info.routeFrom,
                'routeTo': bus_info.routeTo,
                'arriveTime': bus_info.arriveTime,
                'departureTime': bus_info.departureTime,
            }
            booking_details = {
                'TotalAmount': booking.TotalAmount,
                'no_of_passengers_booked': len(booking.passengerDetailsIds),
                'bookingDate': booking.bookingDate,
            }
            travelled_booking = {**bus_details, **booking_details}
            travelled_bookings.append(travelled_booking)
    return travelled_bookings

def booking_id_exists(booking_id):
    return Bookings.objects(id=booking_id).first()

def smsSendingToPhNum(booking_id):
    return Bookings.objects(id=booking_id).first()
