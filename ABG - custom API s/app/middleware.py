import json
import os
from functools import wraps
import requests
from flask import request

from app.utils.response import success_response, error_response


def validate_user(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            payload = {}
            jwt_token = request.headers.get('x-access-token')
            url = os.environ.get('USER_AUTH_URL')
            headers = {'x-access-token': jwt_token, 'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, data=json.dumps(payload))

            if response.status_code == 200:
                current_user = response.json()
                if current_user['data']['role'] in allowed_roles:
                    return fn(current_user, jwt_token, *args, **kwargs)
                else:
                    return error_response(401, 'Access Denied')
            else:
                return error_response(401, 'Unauthorized')
        return wrapper

    return decorator
