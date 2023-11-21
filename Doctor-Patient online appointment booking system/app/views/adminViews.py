from flask import Blueprint

from app.service.adminService import register_doctor,get_Register_Doctor_Records,register_Admin,get_Register_Admin_Records,add_Slot_To_Doctors,update_Slots_status

adminapi_blueprint = Blueprint('adminapi', __name__, url_prefix='/api/admin')
@adminapi_blueprint.route("/registerDoctor",methods=['POST'])
def registerDoctor():
    return register_doctor()

@adminapi_blueprint.route("/getRegisterDoctorRecords",methods=['GET'])
def getRegisterDoctorRecords():
    return get_Register_Doctor_Records()

@adminapi_blueprint.route("/registerAdmin",methods=['POST'])
def registerAdmin():
    return register_Admin()

@adminapi_blueprint.route("/getRegisterAdminRecords",methods=['GET'])
def getRegisterAdminRecords():
    return get_Register_Admin_Records()

@adminapi_blueprint.route("/addSlotToDcotors",methods=['POST'])
def addSloToDoctors():
    return add_Slot_To_Doctors()

@adminapi_blueprint.route("updateSlotStatus/<string:doctorEmailId>",methods=['PUT'])
def updateSlotStatus(doctorEmailId):
    return update_Slots_status(doctorEmailId)

