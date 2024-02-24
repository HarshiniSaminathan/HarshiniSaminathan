from random import randint
from bson import ObjectId
from flask import Blueprint, request, g, Flask, redirect, send_file, jsonify
from app.services.user_service import get_user_detail_by_email,add_device, verify_user, add_user_details, user_device_mapping, user_login, \
    get_users, get_user_detail, user_delete, logout_user, forgot_password, update_user_details, user_bulk_upload, create_user
from app.utils.general_utils import send_email
from app.utils.response import success_response, error_response
import json
from datetime import datetime
from app import mongo, bcrypt
import os
from app.utils.jwt_auth import jwt_token_required

device_blueprint = Blueprint('device', __name__, url_prefix='/api/v1')
user_blueprint = Blueprint('user', __name__, url_prefix='/api/v1')


# login
@user_blueprint.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        code, message, result = user_login(data)
        print(result)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@user_blueprint.route("/logout", methods=['GET'])
@jwt_token_required
def logout(current_user,token):
    try:
        code, message, result = logout_user(current_user)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@user_blueprint.route("/create_user", methods=['POST'])
def insert_user():
    try:
        print("kkkkkk")
        code, message, result = create_user()
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


# add device
@device_blueprint.route('/device', methods=["POST"])
def device():
    """
    Add device details in device table

    """
    try:
        code, message, result = add_device()
        if code == 200:
            return success_response(200, result, "Device Registered")
        else:
            return error_response(400, "Device not registered")
    except Exception as e:
        return error_response(400, str(e))


# add user
@user_blueprint.route('/user', methods=['POST'])
def user():
    try:
        code, message, result = verify_user()
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


# user email verification
@user_blueprint.route('/user/verification', methods=['POST'])
def verification():
    try:
        data = request.get_json()
        verification_type = data.get('type', None)
        token = data.get('token', None)
        email = data.get('email', None)
        password = data.get('password', None)
        if token and email and password:
            verification_details = mongo.db.verification.find_one(
                {"token": token, 'expiration_time': {'$gt': str(datetime.now())}, 'type': verification_type})

            if verification_details and verification_type == 'signup':
                code, message, user_id = add_user_details(verification_details, password)
                if code == 200:
                    return success_response(200, "Verification Successful")
                else:
                    return error_response(400, "Details not added")
            elif verification_details and verification_type == 'forgot_password':
                existing_user = mongo.db.user.find_one({'contact_details.email': email, 'status': 'active'})
                if existing_user:
                    password = bcrypt.generate_password_hash(password).decode('utf-8')
                    update_password = mongo.db.user.update_one({'_id': existing_user['_id']}, {
                        '$set': {'password': password, 'password_update_on': str(datetime.now())}})
                    if update_password:
                        return success_response(200, "Password reset successfully")
                    else:
                        return error_response(400, "Error while updating password")
                else:
                    return error_response(400, "User not found")
            else:
                return error_response(400, "Verification failed")
        else:
            return error_response(400, "Invalid inputs")
    except Exception as e:
        return error_response(400, str(e))


@user_blueprint.route('/forgot_password', methods=['POST'])
@jwt_token_required
def user_forgot_password():
    try:
        data = request.get_json()
        code, message, result = forgot_password(data)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@user_blueprint.route('/user/<user_id>', methods=['PUT'])
@jwt_token_required
def user_update(current_user, user_id):
    try:
        data = request.get_json()
        code, message, result = update_user_details(data, user_id)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@user_blueprint.route('/user', methods=['GET'])
@jwt_token_required
def user_list(current_user):
    try:
        code, message, result, pagination = get_users()
        if code == 200:
            return success_response(200, result, message, pagination)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@user_blueprint.route('/user/<user_id>', methods=['GET'])
@jwt_token_required
def user_details(current_user, user_id):
    try:
        code, message, result = get_user_detail(user_id)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@user_blueprint.route('/user/<user_id>', methods=['DELETE'])
@jwt_token_required
def delete_user(current_user, user_id):
    try:
        code, message, result = user_delete(user_id)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))




@user_blueprint.route('/authorization', methods=['POST'])
@jwt_token_required
def get_user_info(current_user, token):
    try:
        if current_user:
            current_user.pop('password')
            current_user.pop('password_update_on')
            return success_response(200, current_user,token)
        else:
            return success_response(401, {}, "Access Denied !!!")
    except Exception as e:
        return error_response(400, str(e))


@user_blueprint.route('/upload_users', methods=["POST"])
@jwt_token_required
def upload_user(current_user,token):
    try:
        data = request.form.get('device_verification_id')
        code, message, result = user_bulk_upload(data,token)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@user_blueprint.route('/download_incorrect_users', methods=['GET'])
def download_incorrect_users():
    try:
        current_path = os.getcwd()
        filename = current_path + '/user_error_rows.xlsx'
        # Check if the file exists
        if os.path.exists(filename):
            # Send the file as an attachment
            res = send_file(filename, as_attachment=True)
            # Remove the file after sending
            os.remove(filename)
            return res
        else:
            return error_response(400, 'File not found')
    except Exception as e:
        return error_response(400, str(e))


@user_blueprint.route('/user_details/<email_id>', methods=['GET'])
@jwt_token_required
def user_details_by_email(current_user,token,email_id):
    try:
        code, message, result = get_user_detail_by_email(email_id)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))