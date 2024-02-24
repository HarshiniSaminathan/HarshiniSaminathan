from bson import ObjectId
from flask import Blueprint, request, g, jsonify
from app.services.role_services import role, get_role_list, get_permission_list, permissions, role_permission_list
from app.utils.response import success_response, error_response
import json
from datetime import datetime
from app import mongo
from jsonschema import exceptions, ValidationError

role_blueprint = Blueprint('role', __name__, url_prefix='/api/v1')


# add role
@role_blueprint.route('/role', methods=["POST"])
def add_role():
    """
    Add role and store
    :return: access and refresh token
    """
    data = request.json
    try:
        code, message, result = role(data)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except exceptions.ValidationError as err:
        return jsonify({'error': err.message})


# get role list
@role_blueprint.route('/role', methods=["GET"])
def get_rolelist():
    """
    Add role and store
    :return: access and refresh token

    """
    try:
        code, message, result, pagination = get_role_list()
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except exceptions.ValidationError as err:
        return jsonify({'error': err.message})


@role_blueprint.route('/role_permission', methods=["GET"])
def get_role_permission_list():
    """
    Add role and store
    :return: access and refresh token

    """
    try:
        code, message, result, pagination = role_permission_list()
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except exceptions.ValidationError as err:
        return jsonify({'error': err.message})


# get permission list
@role_blueprint.route('/permission', methods=["GET"])
def get_permission_group():
    """
    Get permission group
    :return: access and refresh token

    """
    try:
        code, message, result = get_permission_list()
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except exceptions.ValidationError as err:
        return jsonify({'error': err.message})


# add permissions
@role_blueprint.route('/permission', methods=["POST"])
def add_permission():
    """
    Add permission and store
    :return: access and refresh token
    """
    data = request.json
    try:
        code, message, result = permissions(data)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except exceptions.ValidationError as err:
        return jsonify({'error': err.message})

