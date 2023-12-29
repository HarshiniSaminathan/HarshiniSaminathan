import datetime
from datetime import datetime

from bson import ObjectId

from app.models.busInfoModel import BusInfo
from app.models.bookings import Bookings
from app.models.passengerInfo import PassengerDetails
def check_busInfo_existence(busNumber,arriveTime,departureTime):
    return BusInfo.objects(busNumber=busNumber,arriveTime=arriveTime,departureTime=departureTime).first() is not None

def insert_businfo(busNumber, capacity, routeFrom, routeTo,arriveTime,departureTime,status,amount):

    current_datetime = datetime.utcnow().isoformat()
    busInfo = BusInfo(
        busNumber=busNumber,
        capacity=capacity,
        routeFrom=routeFrom,
        routeTo=routeTo,
        arriveTime=arriveTime,
        departureTime=departureTime,
        status=status,
        created_at=current_datetime,
        amount=amount
    )
    busInfo.save()

def seat_availability(bus_id, seats_selection, booking_date):
    booking_info_list = Bookings.objects(busId=bus_id, bookingDate=booking_date).all()

    for booking_info in booking_info_list:
        passenger_ids = booking_info.passengerDetailsIds

        for passenger_id in passenger_ids:
            passenger_details = PassengerDetails.objects(id=passenger_id).first()
            if seats_selection in passenger_details.seats:
                return False

    return True





def seat_book(bus_id, emailid, contact_number, bookingDate, status, total_amount, ids):
    print(bus_id, emailid, contact_number, bookingDate, status, total_amount, ids,"controller")
    current_datetime = datetime.utcnow().isoformat()
    booking = Bookings(
        busId=bus_id,
        userId=emailid,
        created_at=current_datetime,
        bookingDate=bookingDate,
        contactNumber=contact_number,
        status=status,
        TotalAmount=str(total_amount)
    )
    booking.save()
    Bookings.objects(id=booking.id).update_one(push__passengerDetailsIds=ids)

def bus_id_exists(bus_id):
    return BusInfo.objects(id=bus_id).first()

def bus_no_exists(busNumber):
    return BusInfo.objects(busNumber=busNumber).first()

def check_seats_availability(bus_id, bookingDate):
    bus_info = BusInfo.objects(id=bus_id).first()

    if bus_info:
        no_of_capacity = bus_info.capacity
        bus_info_id = bus_info.id

        total_bookings = Bookings.objects(busId=bus_info_id, bookingDate=bookingDate).all()

        total_passenger_ids = sum(len(booking.passengerDetailsIds) for booking in total_bookings)

        total_seats_availability = int(no_of_capacity) - int(total_passenger_ids)

        return no_of_capacity, total_seats_availability

    return None

