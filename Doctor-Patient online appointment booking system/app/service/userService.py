from flask import request, session
import jwt
from app.controller.userController import check_email_existence, updateSessionCode, deleteSession, \
    check_emailhas_sessionCode
from app.response import failure_response, success_response
from app.controller.userController import loginVerification,OldPasswordExists
from functools import wraps
from datetime import datetime, timedelta
from config import SECRET_KEY
import hashlib

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



def login_user():
    try:
        data = request.get_json()
        required_fields = ['EmailId', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        EmailId = data['EmailId']
        password = data['password']
        if check_email_existence(EmailId):
            userId = loginVerification(EmailId, password)
            if userId:
                for roles in userId:
                    Role = roles.role
                    user_info = {'EmailId': EmailId, 'Role': Role}
                    jwt_token = generate_jwt_token(user_info)
                    jwt_token_str = jwt_token.decode('utf-8')
                    if jwt_token_str:
                        session_code = generate_session_code(user_info={'EmailId': EmailId, 'Role': Role})
                        print("session-CODE-LOGIN",session_code)
                        updateSessionCode(EmailId,session_code)   # session Code add in the USER TABLE
                        return success_response({"data": Role, "token": jwt_token_str})
                    else:
                        return failure_response(statuscode='400', content='User Invalid')
            else:
                return failure_response(statuscode='400', content="Password Invalid")
        else:
            return failure_response(statuscode='400', content=f'EmailId does not found')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def change_Password():
    try:
        data = request.get_json()
        required_fields = ['EmailId', 'OldPassword', 'NewPassword']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        EmailId = data['EmailId']
        OldPassword = data['OldPassword']
        NewPassword = data['NewPassword']
        if check_email_existence(EmailId):
            if OldPasswordExists(EmailId, OldPassword):
                try:
                    from app.controller.userController import change_Password
                    change_Password(EmailId, NewPassword)
                    return success_response('Password updated successfully')
                except Exception as e:
                    print(f"Error: {e}")
                    return failure_response(statuscode='500', content='An unexpected error occurred.')
            else:
                return failure_response(statuscode='500', content='Current Password Invalid')
        return failure_response(statuscode='409', content=f'EmailId: {EmailId} does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')

def forgot_Password():
    try:
        from app.utils.emailSender import otpSending
        data = request.get_json()
        required_fields = ['EmailId']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        EmailId = data['EmailId']
        if check_email_existence(EmailId):
            try:
                global_otp, global_Email = otpSending(EmailId)
                print(global_Email, global_otp)
                session['global_OTP'] = global_otp
                session['global_EMAILID'] = global_Email
                return success_response('OTP sent Successfully')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content='An unexpected error occurred.')
        return failure_response(statuscode='409', content=f'EmailId: {EmailId} does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def verify_Otp():
    try:
        data = request.get_json()
        required_fields = ['OTP', 'EmailId']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        EmailId = data['EmailId']
        OTP = data['OTP']
        print(EmailId, OTP)
        if check_email_existence(EmailId):
            stored_otp = session.get('global_OTP')
            stored_email = session.get('global_EMAILID')
            if check_email_existence(EmailId) and EmailId == stored_email and OTP == stored_otp:
                return success_response('OTP Valid')
            else:
                return failure_response(statuscode='500', content='Invalid OTP')
        return failure_response(statuscode='409', content=f'EmailId: {EmailId} does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def change_Password_By_Otp():
    try:
        data = request.get_json()
        required_fields = ['EmailId', 'NewPassword']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        EmailId = data['EmailId']
        NewPassword = data['NewPassword']
        if check_email_existence(EmailId):
            try:
                from app.controller.userController import change_Password
                change_Password(EmailId, NewPassword)
                return success_response('Password updated successfully')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content='An unexpected error occurred.')
        return failure_response(statuscode='409', content=f'EmailId: {EmailId} does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')



