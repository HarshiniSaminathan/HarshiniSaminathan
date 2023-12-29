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
    booking_info = Bookings.objects(busId=bus_id, bookingDate=booking_date).first()
    if booking_info:
        passenger_ids = booking_info.passengerDetailsIds

        for passenger_id in passenger_ids:
            passenger_details = PassengerDetails.objects(id=passenger_id).first()
            if seats_selection in passenger_details.seats:
                return False
        return True

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

