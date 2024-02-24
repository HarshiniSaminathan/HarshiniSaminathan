# Import required modules
import datetime
from datetime import timedelta
import json
from functools import wraps

from bson import ObjectId
from flask import current_app, request, jsonify, g
from app import config, mongo
import jwt
from app import mongo
from bson.objectid import ObjectId
# from app.config import SECRET_KEY

from app.utils.response import success_response


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
def get_jwt_token(device_id, session_code=None):
    try:
        token = {}
        access_token_data = {"device_id": str(device_id),
                             'iat': datetime.datetime.utcnow(),
                             "exp": get_auth_exp(config.JWT_ACCESS_TOKEN_EXPIRY_IN_MINUTES)}

        refresh_token_data = {"device_id": device_id,
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
        return None


def get_auth_exp(timeout_in_minutes):
    try:
        ts = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout_in_minutes)
        return ts
    except Exception as err:
        return None


def get_jwt(user_id, org_id, session_code=None):
    try:
        user_id = str(user_id)
        access_token_data = {'user_id': str(user_id), 'org_id': org_id, 'iat': datetime.datetime.utcnow(),
                             "exp": datetime.datetime.utcnow() + datetime.timedelta(
                                 minutes=int(config.JWT_REFRESH_TOKEN_EXPIRY_IN_MINUTES))}
        if session_code:
            access_token_data['session_code'] = session_code
        access_token = jwt.encode(access_token_data, str(config.SECRET_KEY), algorithm='HS256')
        token = {"access_token": access_token}

        if session_code:
            refresh_token_data = {'user_id': user_id, 'org_id': org_id,
                                  'iat': datetime.datetime.utcnow(),
                                  "exp": datetime.datetime.utcnow() + datetime.timedelta(
                                      minutes=int(config.JWT_REFRESH_TOKEN_EXPIRY_IN_MINUTES)),
                                  'session_code': session_code}

            refresh_token = jwt.encode(refresh_token_data, str(config.SECRET_KEY), algorithm='HS256')
            token['refresh_token'] = refresh_token
        return token
    except Exception as err:
        return None


def jwt_token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get('x-access-token')

            
            # return 401 if token is not passed
            if not token:
                return jsonify({'message': 'Token is missing !!'}), 401
            data = jwt.decode(token, str(config.SECRET_KEY), algorithms=['HS256'])
            user_id = data.get('user_id')
            session_code = data.get('session_code')
            if session_code:
                # user_device_mapping = mongo.db.user_device.find_one(
                #     {"user_id": ObjectId(user_id), "session_code": session_code, "status": "active"})
                # if user_device_mapping:
                #     user_device = mongo.db.device.find_one(
                #         {"_id": ObjectId(user_device_mapping['device_id']), "status": "active"})
                user_exist = mongo.db.user.find_one({"session_code": session_code})
                if user_exist:
                    g.session_code = session_code
            current_user = mongo.db.user.find_one({"_id": ObjectId(user_id), "status": "active"})
            if current_user:
                current_user['_id'] = str(current_user['_id'])
                current_user['session_code'] = session_code
            # checking the method and endpoint for permission
            
            if request.method == 'POST' :
                payload_data=request.json

                if payload_data:
                    payload = request.json
                    if payload and 'path' and 'method' in payload:
                        path = payload['path']
                        method = payload['method']
                    else:
                        path = request.url_rule.rule
                        path = path.split('/api/v1')[1]
                        method = request.method
                    if path and method:
                        permission = mongo.db.role_permissions.find_one({'role_name': current_user['role'], 'permissions': {
                            '$elemMatch': {'endpoint': path, 'method': method}}})
                        if permission:
                            return fn(current_user, token, *args, **kwargs)
                        else:
                            return success_response(401, {}, "Access Denied !!!")
                    else:
                        return success_response(401, {}, "Access Denied !!!")
                else:
                    return fn(current_user, token, *args, **kwargs)
            else:
                return fn(current_user, token, *args, **kwargs)
        except Exception as e:
            print(e)
            return jsonify({"msg": "Something went wrong !!!"}), 401

    return wrapper


# def jwt_token_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         try:
#             token = request.headers.get('x-access-token')
#             # return 401 if token is not passed
#             if not token:
#                 return jsonify({'message': 'Token is missing !!'}), 401
#             data = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
#             user_id = data.get('user_id')
#             session_code = data.get('session_code')
#
#             if session_code:
#                 user_device_mapping = mongo.db.user_device.find_one(
#                     {"user_id": ObjectId(user_id), "session_code": session_code, "status": "active"})
#
#                 if user_device_mapping:
#                     user_device = mongo.db.device.find_one(
#                         {"_id": ObjectId(user_device_mapping['device_id']), "status": "active"})
#                     if user_device:
#                         g.session_code = session_code
#             current_user = mongo.db.user.find_one({"_id": ObjectId(user_id), "status": "active", "deleted_at": None})
#             if current_user:
#                 current_user['_id'] = str(current_user['_id'])
#             path = request.args.get('path')
#             method = request.args.get('method')
#             if not path and not method:
#                 path = request.url_rule.rule
#                 path = path.split('/api/v1')[1]
#                 method = request.method
#             if path and method:
#                 permission = mongo.db.role_permission.find_one({'role_name': current_user['role'], 'permissions': {
#                     '$elemMatch': {'endpoint': path, 'method': method}}})
#                 if permission:
#                     return fn(current_user, *args, **kwargs)
#                 else:
#                     return success_response(401, {}, "Access Denied !!!")
#             else:
#                 return success_response(401, {}, "Access Denied !!!")
#         except Exception as e:
#             return jsonify({"msg": "Missing or invalid token"}), 401
#     return wrapper
