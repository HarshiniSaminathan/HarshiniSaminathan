from flask import Blueprint

from app.service.busService import add_bus_Info, seat_Availability_For_BusNo

busapi_blueprint = Blueprint('busapi', __name__, url_prefix='/api/bus')

@busapi_blueprint.route('busInfo',methods=['POST'])
def busInfo():
    return add_bus_Info()

@busapi_blueprint.route('seatAvailabilityForBusNo',methods=['GET'])
def seatAvailabilityForBusNo():
    return seat_Availability_For_BusNo()

