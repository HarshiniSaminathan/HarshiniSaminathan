from flask import Blueprint

from app.service.patientService import register_New_Patient,get_Available_Doctors,profile_upadte,get_slotsfor_doctor,requesting_for_appointment,get_patient_appointments,count_appointments

patientapi_blueprint = Blueprint('patientapi', __name__, url_prefix='/api/patient')

@patientapi_blueprint.route("/registerNewPatient",methods=['POST'])
def registerNewPatient():
    return register_New_Patient()

@patientapi_blueprint.route("getAvailableDcotors")
def getAvailableDoctors():
    return get_Available_Doctors()
@patientapi_blueprint.route("/profileUpdate/<string:patientEmailId>",methods=['PUT'])
def profileUpdate(patientEmailId):
    return profile_upadte(patientEmailId)

@patientapi_blueprint.route("/getAllSlotsforDcotor/<string:doctorEmailId>",methods=['GET'])
def getAllSlotsforDcotor(doctorEmailId):
    return get_slotsfor_doctor(doctorEmailId)

@patientapi_blueprint.route("requestingForAppointmnet/<string:patientEmailId>",methods=['POST'])
def requestingForAppoinmnets(patientEmailId):
    return requesting_for_appointment(patientEmailId)

@patientapi_blueprint.route("getPatientAppointments/<string:patientEmailId>",methods=['GET'])
def getDoctorAppointments(patientEmailId):
    return get_patient_appointments(patientEmailId)

@patientapi_blueprint.route("getAppointmentsCount/<string:patientEmailId>",methods=['GET'])
def getAppointmentsCount(patientEmailId):
    return count_appointments(patientEmailId)



