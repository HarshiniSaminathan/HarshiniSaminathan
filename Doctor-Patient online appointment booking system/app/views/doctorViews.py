from flask import Blueprint

from app.service.doctorService import responding_for_appointment,get_doctor_appointments,count_appointments
doctorapi_blueprint = Blueprint('doctorapi', __name__, url_prefix='/api/doctor')
@doctorapi_blueprint.route("ResponseForAppointmnets/<string:doctorEmailId>",methods=['PUT'])
def ResponseForAppointmnets(doctorEmailId):
    return responding_for_appointment(doctorEmailId)

@doctorapi_blueprint.route("getDoctorAppointments/<string:doctorEmailId>",methods=['GET'])
def getDoctorAppointments(doctorEmailId):
    return get_doctor_appointments(doctorEmailId)


@doctorapi_blueprint.route("getAppointmentsCount/<string:doctorEmailId>",methods=['GET'])
def getAppointmentsCount(doctorEmailId):
    return count_appointments(doctorEmailId)