import hashlib
import logging
import os
import re
import random
import string
import uuid
from datetime import datetime, timedelta
import jwt
from flask import jsonify, current_app
from flask_mail import Mail, Message
from app import mail
from bson import ObjectId
from app.utils.helpers import schema_validator
from app import mongo


def generate_password_hash(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


def generate_random_string(length: int = 32) -> str:
    """Generate a random string of the given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_uuid() -> str:
    """Generate a UUID."""
    return str(uuid.uuid4())


def secure_filename(filename: str) -> str:
    """Return a secure version of the given filename."""
    # Use werkzeug's secure_filename function
    from werkzeug.utils import secure_filename
    return secure_filename(filename)


def get_env_variable(name: str) -> str:
    """Get the value of an environment variable or raise an exception."""
    value = os.getenv(name)
    if not value:
        raise Exception(f'Missing required environment variable: {name}')
    return value


def format_datetime(dt: datetime, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """Format a datetime object as a string."""
    return dt.strftime(fmt)


def is_valid_email(email):
    # Simplified regex for basic email validation
    email_regex = r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'
    return bool(re.match(email_regex, email))


def is_valid_phone_number(phone):
    phone_regex = r'^\d{10}$'
    return bool(re.match(phone_regex, str(phone)))


def sanitize_input(input_string):
    """Sanitize the given input string"""
    # Code to sanitize input
    pass


def paginate(items, page=1, per_page=10):
    """Paginate the given items"""
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]


def generate_token(user_id):
    """Generate a JWT token"""
    payload = {'user_id': user_id}
    secret_key = current_app.config.get('SECRET_KEY')
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token.decode('utf-8')


def decode_token(token):
    """Decode a JWT token"""
    secret_key = current_app.config.get('SECRET_KEY')
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please login again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please login again.'


def generate_unique_id():
    """Generate a unique ID"""
    return str(uuid.uuid4())


def get_logger():
    """Get a logger object"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def json_response(status_code, message=None, data=None):
    """Return a JSON response"""
    payload = {'status': status_code}
    if message:
        payload['message'] = message
    if data:
        payload['data'] = data
    return jsonify(payload), status_code


def generate_session_code():
    try:
        n = 8
        from random import randint
        random_number = ''.join(["%s" % randint(0, 9) for num in range(0, n)])
        return random_number
    except Exception as err:
        return None


def create_new_session(user_id, device_id=None):
    session_code = generate_session_code()
    if device_id:
        user_device = mongo.db.device.find_one({'_id': ObjectId(device_id)})
        if user_device:
            user_device_mapping = {'user_id': user_id, 'device_id': ObjectId(device_id), 'session_code': session_code,
                                   'status': 'active', 'is_active': True, 'login_at': datetime.now(), 'logout_at': None,
                                   'deleted_at': None}
            mongo.db.user_device.insert_one(user_device_mapping)
            return session_code
        else:
            return None
    return session_code


def send_email(verification_type, payload):
    current_time = datetime.now()
    expiration_time = str(current_time + timedelta(hours=1))
    verification_code = ''.join(random.choices(string.digits, k=6))
    # verification_link = f'http://localhost:5000/api/v1/user/verification/{verification_code}'
    # verification_link = f'http://localhost:3000/reset-password/{email}?token={verification_code}'
    verification_link = ""

    # Add verification code and link to payload
    verification_data = {}
    verification_data['token'] = verification_code
    verification_data['verification_link'] = verification_link
    verification_data['expiration_time'] = expiration_time

    # Insert new document in verification collection
    verification_data['attempts'] = 0
    verification_data['type'] = verification_type
    verification_data['created_at'] = str(datetime.now())
    verification_data['updated_at'] = str(datetime.now())
    if verification_type == 'signup':
        verification_data['payload'] = payload
    else:
        verification_data['payload'] = {}

    # check the validation
    print()
    is_validated = schema_validator(verification_data, 'verification_model.json')
    if not is_validated:
        result = mongo.db.verification.insert_one(verification_data)
        inserted_id = str(result.inserted_id)

        # send mail
        email = payload['email']
        msg = Message('Email verification', recipients=[email])
        msg.body = f'Please click the following link within 1 hour to verify your email: {verification_link}'
        mail.send(msg)
        return inserted_id
    else:
        return 200, 'Validation Failed', {}

