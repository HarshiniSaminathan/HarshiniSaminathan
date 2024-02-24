from flask import jsonify
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound, InternalServerError

def handle_api_error(error):
    """
    Handles API errors and returns an error response.

    :param error: The error that occurred.
    :return: An error response with the error message and status code.
    """
    error_code = getattr(error, "code", 500)
    error_name = getattr(error, "name", "Internal Server Error")
    error_description = str(error)

    response = {
        "error": {
            "code": error_code,
            "name": error_name,
            "description": error_description
        }
    }

    return jsonify(response), error_code

def bad_request(message):
    """
    Raises a 400 Bad Request error with a custom error message.

    :param message: The error message to include in the response.
    """
    raise BadRequest(message)

def unauthorized(message):
    """
    Raises a 401 Unauthorized error with a custom error message.

    :param message: The error message to include in the response.
    """
    raise Unauthorized(message)

def forbidden(message):
    """
    Raises a 403 Forbidden error with a custom error message.

    :param message: The error message to include in the response.
    """
    raise Forbidden(message)

def not_found(message):
    """
    Raises a 404 Not Found error with a custom error message.

    :param message: The error message to include in the response.
    """
    raise NotFound(message)

def internal_server_error(message):
    """
    Raises a 500 Internal Server Error with a custom error message.

    :param message: The error message to include in the response.
    """
    raise InternalServerError(message)
