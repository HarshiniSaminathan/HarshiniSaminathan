from flask import Blueprint
adminapi_blueprint = Blueprint('adminapi', __name__)
from app.service.adminService import register_doctor,get_Register_Doctor_Records,register_Admin,get_Register_Admin_Records

@adminapi_blueprint.route("/api/admin/registerDoctor",methods=['POST'])
def registerDoctor():
    return register_doctor()

@adminapi_blueprint.route("api/admin/getRegisterDoctorRecords",methods=['GET'])
def getRegisterDoctorRecords():
    return get_Register_Doctor_Records()

@adminapi_blueprint.route("api/admin/registerAdmin",methods=['POST'])
def registerAdmin():
    return register_Admin()

@adminapi_blueprint.route("api/admin/getRegisterAdminRecords")
def getRegisterAdminRecords():
    return get_Register_Admin_Records()
