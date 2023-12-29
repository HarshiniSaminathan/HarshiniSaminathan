from datetime import datetime

from flask import request

from app.controller.busController import seat_book, bus_id_exists, seat_availability
from app.controller.userController import check_email_existence, insert_user, save_passenger
from app.models.bookings import Bookings
from app.models.passengerInfo import PassengerDetails
from app.response import failure_response, success_response


def user_sign_up():
    try:
        data=request.get_json()
        required_fields = ['emailid', 'password', 'fullname']
        if required_fields:
            for field in required_fields:
                if field not in data or not data[field]:
                    return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
            emailid = data['emailid']
            password = data['password']
            fullname = data['fullname']
            role = "USER"
            if not check_email_existence(emailid):
                insert_user(emailid, password, fullname, role)
                return success_response('User Added Successfully')
            return failure_response(statuscode='409', content='Email id already exists')
        return failure_response(statuscode='409', content='required_fields Not found')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def save_passenger(passenger_info):
    passenger = PassengerDetails(
        seats=passenger_info.get('seats'),
        passenger_names=passenger_info.get('passenger_Names'),
        gender=passenger_info.get('gender'),
        age=passenger_info.get('age'),
        id_proof_type=passenger_info.get('IDProofType'),
        id_proof=passenger_info.get('IdProof')
    )
    passenger.save()
    return str(passenger.id)


def bus_booking():
    try:
        data = request.get_json()
        bus_id = data.get('bus_id')
        emailid = data.get('emailid')
        contact_number = data.get('contact_number')
        booking_date = data.get('bookingDate')
        status = data.get('status', 'ACCEPTED')
        passengers_info = data.get('passenger_info', [])
        total_pass = len(passengers_info)
        current_datetime = datetime.utcnow().isoformat()
        if bus_id_exists(bus_id):
            if check_email_existence(emailid):
                seats_selection = get_seats_selection(passengers_info)
                print("seats_selection",seats_selection)

                not_available_seats=[]
                for seats in seats_selection:
                    seat_availability_result = seat_availability(bus_id,seats,booking_date)

                    print(seat_availability_result,'seat_availability_result')
                    if not seat_availability_result:
                        not_available_seats.append(seats)

                print(not_available_seats)
                if len(not_available_seats)==0:
                    amountForbusId = bus_id_exists(bus_id)
                    total_amount = int(total_pass) * int(amountForbusId.amount)

                    booking = Bookings(
                        busId=bus_id,
                        userId=emailid,
                        created_at=current_datetime,
                        bookingDate=booking_date,
                        contactNumber=contact_number,
                        status=status,
                        TotalAmount=str(total_amount)
                    )

                    passenger_ids = [save_passenger(passenger_info) for passenger_info in passengers_info]

                    booking.passengerDetailsIds.extend(passenger_ids)
                    booking.save()

                    return success_response({'message': 'Booking created successfully'})
                else:
                    return failure_response('400', f'Seats not available for the selected passengers {not_available_seats}')

            return failure_response('500', 'Email does not exist')
        return failure_response('500', f'Bus Not Found {bus_id}')

    except Exception as e:
        return failure_response(500, {'error': f'An unexpected error occurred: {str(e)}'})

def get_seats_selection(passengers_info):
    seats_selection = [passenger_info.get('seats') for passenger_info in passengers_info]
    return seats_selection