
from flask import Blueprint
from app.service.user_service import get_users, add_user, check_email, edit_user, delete_user_route,validate_user_email,validate_user_password

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/", methods=['GET'])
def home():
    return get_users()

@api_blueprint.route('/adduser', methods=['POST'])
def adduser():
    return add_user()

@api_blueprint.route("/checkmail/<string:emailid>", methods=['GET'])
def checkmail(emailid):
    return check_email(emailid)

@api_blueprint.route("/editUser/<string:emailid>", methods=['GET', 'PUT'])
def edituser(emailid):
    return edit_user(emailid)

@api_blueprint.route("/deleteUser/<string:emailid>", methods=['DELETE'])
def deleteUser(emailid):
    return delete_user_route(emailid)

@api_blueprint.route("/validateemail/<string:emailid>",methods=['GET'])
def validateemail(emailid):
    return validate_user_email(emailid)

@api_blueprint.route("/validatepassword",methods=['GET'])
def validatepassword():
    return validate_user_password()