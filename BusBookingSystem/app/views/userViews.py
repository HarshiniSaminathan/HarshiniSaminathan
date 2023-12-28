from flask import Blueprint


from app.service.userService import user_sign_up,bus_booking

userapi_blueprint = Blueprint('userapi', __name__, url_prefix='/api/user')

@userapi_blueprint.route('signUp',methods=['POST'])
def signup():
    return user_sign_up()

@userapi_blueprint.route('busBooking',methods=['POST'])
def busBooking():
    return bus_booking()

