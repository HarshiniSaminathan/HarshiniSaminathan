from flask import Blueprint, request

from app.middleware import validate_user
from app.services.notification_service import send_notification, notification_list
from app.utils.response import success_response, error_response

notification_blueprint = Blueprint('notification', __name__, url_prefix='/api/v1')


@notification_blueprint.route('/notification', methods=['POST'])
@validate_user(['admin'])
def notification(current_user, token):
    try:
        data = request.get_json()
        code, message, result = send_notification(data, token)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@notification_blueprint.route("/notification", methods=['GET'])
@validate_user(['employee', 'initiator', 'admin'])
def get_notification_list(current_user, token):
    try:
        code, message, result = notification_list(current_user)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))
