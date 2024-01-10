from flask import Blueprint

from app.service.doctorService import (responding_for_appointment, get_All_PMReports,
                                       get_doctor_appointments, count_appointments, add_Prescription,
                                       response_For_Feedback_, get_All_Feedbacks, return_filename, download_files)
from app.service.userService import token_required

doctorapi_blueprint = Blueprint('doctorapi', __name__, url_prefix='/api/doctor')
@doctorapi_blueprint.route("ResponseForAppointmnets/<string:doctorEmailId>",methods=['PUT'])
@token_required(['DOCTOR'])
def ResponseForAppointmnets(doctorEmailId):
    return responding_for_appointment(doctorEmailId)

@doctorapi_blueprint.route("getDoctorAppointments/<string:doctorEmailId>",methods=['GET'])
@token_required(['DOCTOR'])
def getDoctorAppointments(doctorEmailId):
    print(doctorEmailId)
    return get_doctor_appointments(doctorEmailId)

@doctorapi_blueprint.route("getAppointmentsCount/<string:doctorEmailId>",methods=['GET'])
@token_required(['DOCTOR'])
def getAppointmentsCount(doctorEmailId):
    return count_appointments(doctorEmailId)

@doctorapi_blueprint.route("addPrescription",methods=['POST'])
@token_required(['DOCTOR'])
def addPrescription():
    return add_Prescription()
@doctorapi_blueprint.route("getAllFeedback",methods=['GET'])
@token_required(['DOCTOR'])
def getAllFeedback():
    return get_All_Feedbacks()
@doctorapi_blueprint.route("responseForFeedback",methods=['POST'])
@token_required(['DOCTOR'])
def responseForFeedback():
    return response_For_Feedback_()

@doctorapi_blueprint.route("/getAllPMReports",methods=['GET'])
@token_required(['DOCTOR'])
def getAllPMReports():
    return get_All_PMReports()

@doctorapi_blueprint.route("/returnFilename",methods=['GET'])
@token_required(['DOCTOR'])
def returnFilename():
    return return_filename()

@doctorapi_blueprint.route("/downloadPMReports",methods=['GET'])
def downloadPMReports():
    return download_files()


