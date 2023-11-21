from flask import Blueprint

from app.service.doctorService import responding_for_appointment
doctorapi_blueprint = Blueprint('doctorapi', __name__, url_prefix='/api/doctor')
@doctorapi_blueprint.route("ResponseForAppointmnets/<string:doctorEmailId>",methods=['PUT'])
def ResponseForAppointmnets(doctorEmailId):
    return responding_for_appointment(doctorEmailId)