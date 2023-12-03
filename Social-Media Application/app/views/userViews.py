from flask import Blueprint

from app.service.userService import user_Sign_Up, login, addProfile, token_required, log_Out

userapi_blueprint = Blueprint('userapi', __name__, url_prefix='/api/user')


@userapi_blueprint.route("signUp",methods=['POST'])
def userSignUp():
    return user_Sign_Up()

@userapi_blueprint.route("login",methods=['GET'])
def user_login():
    return login()


@userapi_blueprint.route("AddProfile",methods=['POST'])
@token_required(['USER'])
def add_Profile():
    return addProfile()


@userapi_blueprint.route("logout",methods=['GET'])
@token_required(['USER'])
def logout():
    return log_Out()




