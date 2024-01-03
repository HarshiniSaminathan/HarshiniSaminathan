import os.path
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
from sqlalchemy import text, create_engine
from werkzeug.utils import secure_filename

from app.response import failure_response, success_response

SECRET_KEY ='admin123'

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#   Master database (for write operations)
master_uri = 'postgresql://postgres:Harshini%402003@localhost:5432/write_replica'
app.config['SQLALCHEMY_DATABASE_URI'] = master_uri
db = SQLAlchemy(app)

#   Read replica database (for read operations)
read_replica_uri = 'postgresql://postgres:Harshini%402003@localhost:5432/read_replica'
read_replica_engine = create_engine(read_replica_uri)

UPLOAD_FOLDER = "/home/divum/Downloads/new_training/HarshiniSaminathan/readReplica/Files"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=True)
    password = db.Column(db.String(30), nullable=True)
    userinfo = db.relationship('UserInfo', back_populates='user', uselist=False, cascade='all, delete-orphan')


class UserInfo(db.Model):
    __tablename__ = 'Userinfo'
    infoId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(30), unique=True, nullable=True)
    phonenumber = db.Column(db.String(30), nullable=True)
    DOB = db.Column(db.Date, nullable=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    user = db.relationship('User', back_populates='userinfo', uselist=False)



with app.app_context():
    db.create_all()


def token_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return failure_response('401', 'Token is missing')
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                username = payload['username']
                exp = payload['exp']
                if not username_exists(username):
                    return failure_response(500,'User not found')

            except jwt.ExpiredSignatureError:
                return failure_response('401', 'Token has expired')

            except jwt.InvalidTokenError:
                return failure_response('401', 'Invalid token')
            return func(*args, **kwargs)
        return wrapper
    return decorator

def username_exists(username):
    count = User.query.filter_by(username=username).count()
    return count > 0

@app.route('/write', methods=['POST'])
# @token_required()
def write_operation():
    try:
        data = request.get_json()
        required_fields = ['username', 'password','address','phonenumber','DOB']

        for field in required_fields:
            if field not in data:
                return failure_response(500, f"{field}: Missing fields")

        username = data['username']
        password = data['password']
        address = data['address']
        phonenumber = data['phonenumber']
        DOB = data['DOB']

        if not username_exists(username):
            # Create User and associated UserInfo
            new_user = User(username=username, password=password)
            new_user_info = UserInfo()
            new_user.userinfo = new_user_info
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()
            userid = User.query.filter_by(username=username).first()
            id=userid.id

            new_info = UserInfo.query.filter_by(userid=id)
            if new_info:
                for info in new_info:
                    info.address=address
                    info.phonenumber=phonenumber
                    info.DOB=DOB
                    db.session.commit()


            return success_response('Write operation successful')
        else:
            return failure_response(500, 'Username already exists')

    except IntegrityError:
        db.session.rollback()  # Rollback the transaction if IntegrityError occurs (e.g., duplicate entry)
        return failure_response(500, {'message': 'Username already exists'})

    except NoResultFound:
        db.session.rollback()  # Rollback the transaction if NoResultFound occurs
        return failure_response(500, {'message': 'Error in write operation: NoResultFound'})

    except SQLAlchemyError as e:
        return failure_response(500, {'message': f'Error in write operation: {e}'})



@app.route('/read', methods=['GET'])
def read_operation():
    try:
        with app.app_context():
            users = User.query.all()
            info = UserInfo.query.all()
        user_list = [{'id': user.id, 'username': user.username ,'address': infos.address,'DOB':infos.DOB,'phonenumber':infos.phonenumber} for user in users for infos in info]
        return success_response({'users': user_list})

    except SQLAlchemyError as e:
        return failure_response(500,f'Error in read operation: {e}')

@app.route('/display',methods=['GET'])
def display():
    try:
        data= request.get_json()
        required_feilds=['username']
        for field in required_feilds:
            if field not in required_feilds:
                return failure_response({"message": f"{field}: Missing fields"})
        username=data['username']
        if username_exists(username):
            data= User.query.filter_by(username=username).first()
            array=[]
            array.append(
                {
                    "s.no": data.id,
                    "username": data.username
                }
            )
            return success_response(array)
        return failure_response(500,{'message':'Username Does Not Exists'})
    except SQLAlchemyError as e:
        return failure_response(500,{'message': f'Error in read operation: {e}'})

@app.route('/uploadFiles',methods=['POST'])
def uploadFiles():
    try:
        import uuid
        files=request.files['file']
        if files:
            file_name=secure_filename(files.filename)
            temp_filename = str(uuid.uuid1()) + str(file_name)
            print(temp_filename)
            files.save(os.path.join(UPLOAD_FOLDER,temp_filename))
            return success_response({'message':'Uploaded Successfully'})
        else:
            return failure_response(500,{'message':'File Not Found'})
    except SQLAlchemyError as e:
        return success_response({'message':f'Error in Uploading,{e}'})

@app.route('/displayFiles',methods=['GET'])
def displayFiles():
    try:
        data=request.get_json()
        required_fields=['filename']
        for fields in required_fields:
            if fields not in data:
                return jsonify({"message": f"{fields}: Missing fields"})
        filename=data['filename']
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        return send_file(filepath,as_attachment=True)
    except NotImplementedError as e:
        return jsonify({'message':f'Error in Downloading file {e}'})


def check_login_credentials(username, password):
    user = User.query.filter_by(username=username,password=password).first()
    if user:
        return True
    else:
        return False

def generate_token(username):
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    payload = {
        'username': username,
        'exp': expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


@app.route('/login')
def login():
    try:
        data=request.get_json()
        required_feilds=['username','password']
        for field in required_feilds:
            if field not in data:
                return jsonify({"message": f"{field}: Missing fields"})
        username=data['username']
        password = data['password']
        if check_login_credentials(username,password):
            token= generate_token(username)
            jwt_token_str = token.decode('utf-8')
            print(jwt_token_str.split("."))
            return ({"token":jwt_token_str})
        else:
            return jsonify({'message':  'Credentials Failed'})
    except SQLAlchemyError as e:
        return jsonify({'message':  f'Error in login,{e}'})

@app.route('/logout')
def logout():
    try:
        data=request.get_json()
        required_feilds=['username','password']
        for field in required_feilds:
            if field not in data:
                return jsonify({"message": f"{field}: Missing fields"})
        username=data['username']
        password = data['password']
        if check_login_credentials(username,password):
            token= generate_token(username)
            jwt_token_str = token.decode('utf-8')
            print(jwt_token_str.split("."))
            return ({"token":jwt_token_str})
        else:
            return jsonify({'message':  'Credentials Failed'})
    except SQLAlchemyError as error:
        return jsonify({'message':  f'Error in login,{error}'})


if __name__ == '__main__':
    app.run(debug=True, port=5005)