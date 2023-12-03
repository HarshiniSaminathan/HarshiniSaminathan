import json
import os
import hashlib
from functools import wraps

from flask import request
import jwt
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

from app.controller.userController import check_email_existence, insert_user, check_login, check_username_existence, \
    check_email_For_Username, add_profile, updateSessionCode, check_emailhas_sessionCode, deleteSession
from app.response import failure_response, success_response
from config import SECRET_KEY

def generate_session_code(user_info):
    user_info_str = str(user_info)
    hash_object = hashlib.sha256(user_info_str.encode())
    session_code = hash_object.hexdigest()
    return session_code

def generate_jwt_token(user_info):
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    payload = {
        'EmailId': user_info['EmailId'],
        'Role': user_info['Role'],
        'exp': expiration_time,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def user_Sign_Up():
    try:
        data = request.get_json()
        required_fields = ['emailid', 'password', 'username', 'fullname']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        emailid = data['emailid']
        password = data['password']
        username = data['username']
        fullname = data['fullname']
        role = "USER"
        status="INACTIVE"
        if not check_email_existence(emailid):
            if not check_username_existence(username):
                insert_user(emailid, password, username, fullname, role, status)
                return success_response('User Added Successfully')
            return failure_response(statuscode='409', content='UserName already exists')
        return failure_response(statuscode='409', content='Email id already exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def login():
    try:
        data = request.get_json()
        required_fields = ['password', 'emailid']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')

        emailid = data['emailid']
        password = data['password']
        user = check_login(emailid, password)
        if user:
            role = user.role
            user_info = {'EmailId': emailid, 'Role': role}
            jwt_token = generate_jwt_token(user_info)
            jwt_token_str = jwt_token.decode('utf-8')

            if jwt_token_str:
                session_code = generate_session_code(user_info={'EmailId': emailid, 'Role': role})
                print("session-CODE-LOGIN", session_code)
                updateSessionCode(emailid, session_code)  # session Code add in the USER TABLE
                return success_response({"data": role, "token": jwt_token_str})
            else:
                return failure_response(statuscode='400', content='User Invalid')
        else:
            return failure_response(statuscode='400', content='Invalid email or password')

    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')

def log_Out():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                email = payload.get('EmailId')
                Role = payload.get('Role')
                session_code = generate_session_code(user_info={'EmailId': email, 'Role': Role})
                print("session-CODE-LOGOUT", session_code)
                if email:
                    if check_emailhas_sessionCode(email,session_code):
                        deleteSession(email)    # session Code delelte in the USER TABLE
                        return success_response({"message": "Logout successful"})
                    else:
                        return failure_response(statuscode='401', content='Invalid session Code')
            except jwt.ExpiredSignatureError:
                return failure_response(statuscode='401', content='Token has expired')
            except jwt.InvalidTokenError:
                return failure_response(statuscode='401', content='Invalid token')
        return failure_response(statuscode='400', content='Token is missing or invalid')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def addProfile():
    try:
        from run import UPLOAD_FOLDER
        file = request.files['file']
        form_data = request.form.get('data')
        try:
            data = json.loads(form_data)
        except json.JSONDecodeError:
            return failure_response(statuscode='400', content='Invalid JSON data')
        emailid = data['emailid']
        profileName = data['profileName']
        Bio = data['Bio']
        if check_email_For_Username(emailid):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            add_profile(emailid,filename,profileName,Bio)
            return success_response("Profile Added successfully")
        return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def token_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return failure_response(statuscode='401', content='Token is missing')
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                EmailId = payload['EmailId']
                role = payload['Role']

                session_code = generate_session_code(user_info={'EmailId': EmailId, 'Role': role})
                print("session-CODE-API-VERIFY", session_code)

                if role not in allowed_roles:
                    return failure_response(statuscode='403', content=f'Access restricted. User is not authorized')

                if not check_emailhas_sessionCode(EmailId,session_code):   # session Code verifying  in the USER TABLE

                    return failure_response(statuscode='401', content='Token has been invalidated (logged out)')

            except jwt.ExpiredSignatureError:
                return failure_response(statuscode='401', content='Token has expired')
            except jwt.InvalidTokenError:
                return failure_response(statuscode='401', content='Invalid token')

            return func(*args, **kwargs)
        return wrapper
    return decorator