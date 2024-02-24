# Import required modules
import datetime
from datetime import timedelta
import json
from functools import wraps
from flask import current_app, request, jsonify
from app import config
import jwt


# Define commonly used JWT functions
def generate_token(user_id):
    """
    Generate a JWT for a user.

    :param user_id: The ID of the user.
    :return: A string representing the JWT.
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


def decode_token(token):
    """
    Decode a JWT and return the payload.

    :param token: The JWT to decode.
    :return: A dictionary representing the payload of the JWT.
    """
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Token is expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'


def jwt_required(f):
    """
    A decorator function that verifies the JWT in the Authorization header of the request.

    :param f: The function to be decorated.
    :return: The decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401
        try:
            payload = decode_token(token)
            if not isinstance(payload, dict):
                return jsonify({'message': payload}), 401
            user_id = payload.get('user_id')
        except Exception as e:
            return jsonify({'message': 'Token is invalid.'}), 401
        return f(user_id, *args, **kwargs)
    return decorated


#################
def get_jwt_token(device_id,session_code=None):
    try:
        token={}
        access_token_data = {"device_id":str(device_id),
                             'iat': datetime.datetime.utcnow(),
                             "exp": get_auth_exp(config.JWT_ACCESS_TOKEN_EXPIRY_IN_MINUTES)}

        refresh_token_data = {"device_id":device_id,
                              'iat': datetime.datetime.utcnow(),
                              "exp": get_auth_exp(config.JWT_REFRESH_TOKEN_EXPIRY_IN_MINUTES),
                              }

        if session_code:
            access_token_data['session_code'] = session_code
            refresh_token_data['session_code'] = session_code
        access_token = jwt.encode(access_token_data, config.SECRET_KEY, config.JWT_ALGORITHM)
        refresh_token = jwt.encode(refresh_token_data, config.SECRET_KEY, config.JWT_ALGORITHM)
        token = {"access_token": access_token.decode("utf-8")}
        token['refresh_token'] = refresh_token.decode('utf-8')
        return json.dumps(token)
    except Exception as err:
        print("get_jwt_token", err)
        return None


def get_auth_exp(timeout_in_minutes):
    try:
        ts = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout_in_minutes)
        print("************",ts)
        return ts
    except Exception as err:
        return None


def get_jwt(user_id, org_id, session_code=None):
    # try:
    user_id = str(user_id)
    access_token_data = {'identity': str(user_id), 'org_id': org_id, 'iat': datetime.datetime.utcnow(),
                         "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(config.JWT_REFRESH_TOKEN_EXPIRY_IN_MINUTES))}
    if session_code:
        access_token_data['session_code'] = session_code
    access_token = jwt.encode(access_token_data, config.SECRET_KEY, config.JWT_ALGORITHM)
    token = {"access_token": access_token}

    if session_code:
        refresh_token_data = {'identity': user_id, 'org_id': org_id,
                              'iat': datetime.datetime.utcnow(),
                              "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(config.JWT_REFRESH_TOKEN_EXPIRY_IN_MINUTES)),
                              'session_code': session_code}

        refresh_token = jwt.encode(refresh_token_data, config.SECRET_KEY, config.JWT_ALGORITHM)
        token['refresh_token'] = refresh_token
    return token
    # except Exception as err:
    #     print("get_jwt EXCEPTION ===> ", str(err))
    #     return None