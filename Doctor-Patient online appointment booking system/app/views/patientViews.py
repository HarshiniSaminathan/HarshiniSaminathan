from flask import Blueprint

from app.service.patientService import (register_New_Patient,view_prescription,add_Feedback,get_All_Prescription,
                                        get_Available_Doctors,add_PMReports,Check_Slot_Availability_Doctor,get_By_DoctorSpecialization,profile_upadte,get_slotsfor_doctor,requesting_for_appointment,get_patient_appointments,count_appointments)

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
def requestingForAppoinments(patientEmailId):
    return requesting_for_appointment(patientEmailId)

@patientapi_blueprint.route("getPatientAppointments/<string:patientEmailId>",methods=['GET'])
def getDoctorAppointments(patientEmailId):
    return get_patient_appointments(patientEmailId)

@patientapi_blueprint.route("getAppointmentsCount/<string:patientEmailId>",methods=['GET'])
def getAppointmentsCount(patientEmailId):
    return count_appointments(patientEmailId)

@patientapi_blueprint.route("getDoctorsByDoctorSpecialization",methods=['GET'])
def getDoctorsByDoctorSpecialization():
    return get_By_DoctorSpecialization()

@patientapi_blueprint.route("CheckSlotAvailability",methods=['GET'])
def CheckSlotAvailabilityForDoctor():
    return Check_Slot_Availability_Doctor()

@patientapi_blueprint.route("/addPMReports",methods=['POST'])
def addPMReports():
    return add_PMReports()

@patientapi_blueprint.route("/viewPrescription",methods=['GET'])
def viewPrescription():
    return view_prescription()

@patientapi_blueprint.route("addFeedback",methods=['POST'])
def addFeedback():
    return add_Feedback()

@patientapi_blueprint.route("getAllPrescription",methods=['GET'])
def getAllPrescription():
    return get_All_Prescription()
