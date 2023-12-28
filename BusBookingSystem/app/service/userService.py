from flask import request

from app.controller.busController import seat_book
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


def bus_booking():
    try:
        data = request.get_json()
        required_fields = ['bus_id', 'emailid', 'contact_number', 'passenger_info', 'bookingDate']
        if required_fields:
            for field in required_fields:
                if field not in data or not data[field]:
                    return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
            bus_id = data.get('bus_id')
            emailid = data.get('emailid')
            contact_number = data.get('contact_number')
            booking_date = data.get('bookingDate')
            status = data.get('status', 'ACCEPTED')
            passenger_info = data.get('passenger_info', {})
            seats_selection = passenger_info.get('seatsSelection')
            passenger_names = passenger_info.get('passenger_Names')
            gender = passenger_info.get('gender')
            age = passenger_info.get('age')
            id_proof_type = passenger_info.get('IDProofType')
            id_proof = passenger_info.get('IdProof')

            passenger_id = save_passenger(seats_selection, passenger_names, gender, age, id_proof_type, id_proof)
            if passenger_id and passenger_id.id:
                ids = passenger_id.id
                total_amount = "240"
                seat_book(bus_id, emailid, contact_number, booking_date, status, total_amount, ids)
                return success_response({'message': 'Booking created successfully'})
            return failure_response(statuscode='409', content='Error in Booking')
        return failure_response(statuscode='409', content='required_fields Not found')
    except Exception as e:
        return failure_response(500, {'error': f'An unexpected error occurred: {e}'})
