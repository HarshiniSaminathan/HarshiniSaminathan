from flask import Blueprint
from app.service.userService import login_user, change_Password, forgot_Password, verify_Otp, change_Password_By_Otp, \
    log_Out, token_required

loginapi_blueprint = Blueprint('loginapi', __name__, url_prefix='/api/login')

@loginapi_blueprint.route("/",methods=['GET'])
def login():
    return login_user()

@loginapi_blueprint.route("/changePassword",methods=['PUT'])
@token_required(['PATIENT','ADMIN','DOCTOR'])
def changePassword():
    return change_Password()

@loginapi_blueprint.route('forgotPassword',methods=['GET'])
@token_required(['PATIENT','ADMIN','DOCTOR'])
def forgotPassword():
    return forgot_Password()

@loginapi_blueprint.route('verifyOtp',methods=['GET'])
@token_required(['PATIENT','ADMIN','DOCTOR'])
def verifyOtp():
    return verify_Otp()

@loginapi_blueprint.route('changePasswordByOtp',methods=['PUT'])
@token_required(['PATIENT','ADMIN','DOCTOR'])
def changePasswordByOtp():
    return change_Password_By_Otp()

@loginapi_blueprint.route('logOut',methods=['GET'])
def logOut():
    return log_Out()








