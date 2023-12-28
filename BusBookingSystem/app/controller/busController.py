import datetime
from datetime import datetime

from bson import ObjectId

from app.models.busInfoModel import BusInfo
from app.models.bookings import Bookings
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

def seat_availability(bus_id,seats_selection,bookingDate):
    return Bookings.objects(bus_id=bus_id,seats_selection=seats_selection,bookingDate=bookingDate).first() is not None

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
        TotalAmount=total_amount
    )
    booking.save()
    Bookings.objects(id=booking.id).update_one(push__passengerDetailsIds=ids)

