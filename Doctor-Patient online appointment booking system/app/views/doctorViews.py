from flask import Blueprint

from app.service.doctorService import (responding_for_appointment,get_All_PMReports,
                                       get_doctor_appointments,count_appointments,add_Prescription,response_For_Feedback_,get_All_Feedbacks)
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

@doctorapi_blueprint.route("addPrescription",methods=['POST'])
def addPrescription():
    return add_Prescription()
@doctorapi_blueprint.route("getAllFeedback",methods=['GET'])
def getAllFeedback():
    return get_All_Feedbacks()
@doctorapi_blueprint.route("responseForFeedback",methods=['POST'])
def responseForFeedback():
    return response_For_Feedback_()

@doctorapi_blueprint.route("/getAllPMReports",methods=['GET'])
def getAllPMReports():
    return get_All_PMReports()

