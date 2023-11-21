from flask import Blueprint

from app.service.patientService import register_New_Patient,get_Available_Doctors,profile_upadte,get_slotsfor_doctor,requesting_for_appointment

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





