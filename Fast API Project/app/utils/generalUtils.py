import hashlib
import os
import random
import string
import uuid
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from jose import jwt
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRY_MINUTES


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
    """Check if the given string is a valid email"""
    # Code to check email validity
    pass


def is_valid_phone_number(phone_number):
    """Check if the given string is a valid phone number"""
    # Code to check phone number validity
    pass


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


def update_session(user_id, device_id=None):
    session_code = generate_session_code()
    query = {'user_id':user_id}
    if device_id:
        query['device_id'] = device_id
        user_device = mongo.db.user_device.find_one(query)
        if not user_device:
            user_device = {'user_id': user_id, 'device_id': device_id, 'session_code': session_code, 'status': 'active'}
            mongo.db.user_device.insert_one(user_device)
        else:
            user_device['session_code'] = session_code
            mongo.db.user_device.update_one({'_id': user_device['_id']}, {'$set': {'session_code': session_code}})
    else:
        user_devices = mongo.db.user_devices.find(query)
        for user_device in user_devices:
            user_device['session_code'] = session_code
            mongo.db.user_devices.update_one({'_id': user_device['_id']}, {'$set': {'session_code': session_code}})
    return session_code


def generate_request_code():
    prefix = 'SRI'
    random_number = random.randint(1000, 9999)
    return f'{prefix}{random_number}'


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=REFRESH_TOKEN_EXPIRY_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username