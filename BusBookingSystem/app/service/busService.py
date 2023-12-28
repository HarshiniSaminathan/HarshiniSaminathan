from flask import request

from app.controller.busController import check_busInfo_existence, insert_businfo
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

