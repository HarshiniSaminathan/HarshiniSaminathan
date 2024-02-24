# Import required modules
from functools import wraps
from flask import jsonify, request, abort

# Define commonly used decorators
def json_required(f):
    """
    Decorator that ensures that the request contains JSON data.

    :param f: The Flask view function.
    :return: The decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            abort(400, description="Request must contain JSON data.")
        return f(*args, **kwargs)
    return decorated_function

def authenticate(f):
    """
    Decorator that checks if the user is authenticated.

    :param f: The Flask view function.
    :return: The decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is authenticated
        if not current_user.is_authenticated:
            return jsonify({"message": "Authentication required."}), 401
        return f(*args, **kwargs)
    return decorated_function

def authorize(roles):
    """
    Decorator that checks if the user is authorized based on their role.

    :param roles: A list of roles that are authorized to access the view function.
    :return: The decorated function.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if the user is authorized
            if current_user.role not in roles:
                return jsonify({"message": "You are not authorized to access this resource."}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
