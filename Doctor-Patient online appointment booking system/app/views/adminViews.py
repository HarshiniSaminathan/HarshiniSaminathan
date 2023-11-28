from flask import Blueprint

from app.service.adminService import (register_doctor,response_For_Feedback,get_Register_Doctor_Records,get_All_Feedback,
                                      register_Admin,get_Register_Admin_Records,add_Slot_To_Doctors,update_Slots_status)
from app.service.userService import token_required

adminapi_blueprint = Blueprint('adminapi', __name__, url_prefix='/api/admin')

@adminapi_blueprint.route("/registerDoctor",methods=['POST'])
@token_required(['ADMIN'])
def registerDoctor():
    return register_doctor()

@adminapi_blueprint.route("/getRegisterDoctorRecords",methods=['GET'])
@token_required(['ADMIN','DOCTOR','PATIENT'])
def getRegisterDoctorRecords():
    return get_Register_Doctor_Records()

@adminapi_blueprint.route("/registerAdmin",methods=['POST'])
@token_required(['ADMIN'])
def registerAdmin():
    return register_Admin()

@adminapi_blueprint.route("/getRegisterAdminRecords",methods=['GET'])
@token_required(['ADMIN'])
def getRegisterAdminRecords():
    return get_Register_Admin_Records()

@adminapi_blueprint.route("/addSlotToDcotors",methods=['POST'])
@token_required(['ADMIN'])
def addSloToDoctors():
    return add_Slot_To_Doctors()

@adminapi_blueprint.route("updateSlotStatus/<string:doctorEmailId>",methods=['PUT'])
@token_required(['ADMIN','DOCTOR'])
def updateSlotStatus(doctorEmailId):
    return update_Slots_status(doctorEmailId)

@adminapi_blueprint.route("getAllFeedback",methods=['GET'])
@token_required(['ADMIN'])
def getAllFeedback():
    return get_All_Feedback()

@adminapi_blueprint.route("responseForFeedback",methods=['PUT'])
@token_required(['ADMIN'])
def responseForFeedback():
    return response_For_Feedback()
