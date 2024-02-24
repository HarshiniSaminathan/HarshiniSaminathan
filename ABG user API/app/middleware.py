import json
import os
from functools import wraps
import requests
from flask import request


def validate_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        path = request.path
        path = path.split('/api/v1')[1]
        method = request.method
        payload = json.dumps({"path": path, "method": method})
        jwt_token = request.headers.get('x-access-token')
        url = os.environ.get('USER_AUTH_URL')
        headers = {'Authorization': jwt_token, 'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            return fn(True, *args, **kwargs)
        else:
            return {'message': 'Unauthorized'}, 401

    return wrapper
