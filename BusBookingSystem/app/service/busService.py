from flask import request

from app.controller.busController import check_busInfo_existence, insert_businfo, bus_no_exists, \
    check_seats_availability, bus_id_exists
from app.response import failure_response, success_response


def add_bus_Info():
    try:
        data=request.get_json()
        required_fields = ['busNumber', 'capacity', 'routeFrom','routeTo','arriveTime','departureTime','status','amount']
        if required_fields:
            for field in required_fields:
                if field not in data or not data[field]:
                    return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
            busNumber = data['busNumber']
            capacity = data['capacity']
            routeFrom = data['routeFrom']
            routeTo = data['routeTo']
            arriveTime = data['arriveTime']
            departureTime = data['departureTime']
            status = data['status']
            amount = data['amount']
            if not check_busInfo_existence(busNumber,arriveTime,departureTime):
                insert_businfo(busNumber, capacity, routeFrom, routeTo,arriveTime,departureTime,status,amount)
                return success_response('BusInfo Added Successfully')
            return failure_response(statuscode='409', content=f'Already TIME:{arriveTime} to {departureTime} are added for BUS.NO:{busNumber}')
        return failure_response(statuscode='409', content='required_fields Not found')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def seat_Availability_For_BusNo():
    try:
        data = request.get_json()
        required_fields = ['bus_id', 'bookingDate']
        if required_fields:
            for field in required_fields:
                if field not in data or not data[field]:
                    return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
            bus_id = data['bus_id']
            bookingDate = data['bookingDate']
            if bus_id_exists(bus_id):
                Total_seats,available_seats_count=check_seats_availability(bus_id,bookingDate)
                if int(available_seats_count) > 0 :
                    return success_response({'Total_Seats':Total_seats,'available_seats_count':available_seats_count})
                else:
                    return failure_response('500','No available seats')
            else:
                return failure_response('500','Bus Not Found')
        return failure_response(statuscode='409', content='required_fields Not found')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')



