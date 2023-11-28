from flask import Blueprint

from app.controller.patientController import check_for_PMR_beforeDay
from app.service.userService import token_required
from app.service.patientService import (register_New_Patient,view_prescription,add_Feedback,get_All_Prescription,upload_PMReport,
                                        get_Available_Doctors,add_PMReports,Check_Slot_Availability_Doctor,get_By_DoctorSpecialization,profile_upadte,get_slotsfor_doctor,requesting_for_appointment,get_patient_appointments,count_appointments)

patientapi_blueprint = Blueprint('patientapi', __name__, url_prefix='/api/patient')

@patientapi_blueprint.route("/registerNewPatient",methods=['POST'])
@token_required(['PATIENT'])
def registerNewPatient():
    return register_New_Patient()

@patientapi_blueprint.route("/getAvailableDcotors",methods=['GET'])
@token_required(['PATIENT','ADMIN','DOCTOR'])
def getAvailableDoctors():
    return get_Available_Doctors()

@patientapi_blueprint.route("/profileUpdate/<string:patientEmailId>",methods=['PUT'])
@token_required(['PATIENT'])
def profileUpdate(patientEmailId):
    return profile_upadte(patientEmailId)

@patientapi_blueprint.route("/getAllSlotsforDcotor/<string:doctorEmailId>",methods=['GET'])
@token_required(['PATIENT','ADMIN','DOCTOR'])
def getAllSlotsforDcotor(doctorEmailId):
    return get_slotsfor_doctor(doctorEmailId)

@patientapi_blueprint.route("requestingForAppointmnet/<string:patientEmailId>",methods=['POST'])
@token_required(['PATIENT'])
def requestingForAppoinments(patientEmailId):
    return requesting_for_appointment(patientEmailId)

@patientapi_blueprint.route("getPatientAppointments/<string:patientEmailId>",methods=['GET'])
@token_required(['PATIENT'])
def getDoctorAppointments(patientEmailId):
    return get_patient_appointments(patientEmailId)

@patientapi_blueprint.route("getAppointmentsCount/<string:patientEmailId>",methods=['GET'])
@token_required(['PATIENT'])
def getAppointmentsCount(patientEmailId):
    return count_appointments(patientEmailId)

@patientapi_blueprint.route("getDoctorsByDoctorSpecialization",methods=['GET'])
@token_required(['PATIENT','ADMIN','DOCTOR'])
def getDoctorsByDoctorSpecialization():
    return get_By_DoctorSpecialization()

@patientapi_blueprint.route("CheckSlotAvailability",methods=['GET'])
@token_required(['PATIENT','ADMIN','DOCTOR'])
def CheckSlotAvailabilityForDoctor():
    return Check_Slot_Availability_Doctor()

@patientapi_blueprint.route("/addPMReports",methods=['POST']) # done before FILE UPLOADING API (BLOB FORMAT)
@token_required(['PATIENT'])
def addPMReports():
    return add_PMReports()

@patientapi_blueprint.route("uploadPMReport",methods=['POST'])
@token_required(['PATIENT'])
def uploadPMReport():
    return upload_PMReport()

@patientapi_blueprint.route("/viewPrescription",methods=['GET'])
@token_required(['PATIENT'])
def viewPrescription():
    return view_prescription()

@patientapi_blueprint.route("addFeedback",methods=['POST'])
@token_required(['PATIENT'])
def addFeedback():
    return add_Feedback()

@patientapi_blueprint.route("getAllPrescription",methods=['GET'])
@token_required(['PATIENT'])
def getAllPrescription():
    return get_All_Prescription()

@patientapi_blueprint.route("automatedEmailSender",methods=['GET'])
def automatedEmailSender():
    return check_for_PMR_beforeDay()   #  To check Automatic Mail sending is working or NOT


