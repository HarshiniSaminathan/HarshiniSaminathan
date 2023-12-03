from flask import Blueprint
from app.service.adminService import get_All_InactiveUser,activating_The_Users,get_All_ActivatedUsers

adminapi_blueprint = Blueprint('adminapi', __name__, url_prefix='/api/admin')

@adminapi_blueprint.route("getAllInactiveUser",methods=['GET'])
def getAllInactiveUser():
    return get_All_InactiveUser()

@adminapi_blueprint.route("activatingTheUsers",methods=['PUT'])
def activatingTheUsers():
    return activating_The_Users()

@adminapi_blueprint.route("getAllActivatedUsers",methods=['GET'])
def getAllActivatedUsers():
    return get_All_ActivatedUsers()

