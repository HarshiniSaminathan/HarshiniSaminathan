from bson import ObjectId
from flask import Blueprint, request, send_file
import os
from app.middleware import validate_user
from app.services.workflow_service import create_workflow, update_workflow, detail_workflow, \
    list_workflow, delete_workflow, get_schema_list, \
    detail_schema, delete_schema, add_workflow_instance, update_workflow_instance, workflow_instance_list, \
    workflow_instance_details
from app.utils.response import success_response, error_response
import json
from datetime import datetime
from app import mongo, config

from app.utils.s3 import upload_file_to_s3, upload_aws_bucket, delete_file_from_s3
from app.utils.notifications import get_notification_list, mark_all_read

workflow_blueprint = Blueprint('workflow', __name__, url_prefix='/api/v1')
user_blueprint = Blueprint('user', __name__, url_prefix='/api/v1')


# create workflow
@workflow_blueprint.route('/workflow', methods=["POST"])
def workflow():
    """
    Add device details in device table
    """
    try:
        data = request.get_json()
        code, message, result = create_workflow(data)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, "Device not registered")
    except Exception as e:
        return error_response(400, str(e))


# update workflow
@workflow_blueprint.route('/workflow/<id>', methods=["PUT"])
def workflow_update(id):
    """
    Add device details in device table

    """
    try:
        data = request.get_json()
        code, message, result = update_workflow(id, data)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, "Device not registered")
    except Exception as e:
        return error_response(400, str(e))


# workflow list
@workflow_blueprint.route('/workflow', methods=["GET"])
def workflow_list():
    """
    Add device details in device table

    """
    try:
        code, message, result, pagination = list_workflow()
        if code == 200:
            return success_response(200, result, message, pagination=pagination)
        else:
            return error_response(400, "Data Not found")
    except Exception as e:
        return error_response(400, str(e))


# workflow detail
@workflow_blueprint.route('/workflow/<workflow>', methods=["GET"])
def workflow_detail(workflow):
    """
    Add device details in device table

    """
    try:
        code, message, result = detail_workflow(workflow)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, "Device not registered")
    except Exception as e:
        return error_response(400, str(e))


# delete workflow
@workflow_blueprint.route('/workflow/<id>', methods=["DELETE"])
def workflow_delete(id):
    """
    Add device details in device table

    """
    try:
        data = request.get_json()
        code, message, result = delete_workflow(id, data)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, "Device not registered")
    except Exception as e:
        return error_response(400, str(e))


# create document schema/steps
@workflow_blueprint.route('/schema', methods=['POST'])
def create_schema():
    data = request.get_json()
    result = mongo.db.documents.insert_one(data)
    if result:
        return success_response(200, "Document Schema Created")
    else:
        return success_response(200, "Document not created")


# update document schema/steps
@workflow_blueprint.route('/schema/<schema>', methods=['PUT'])
def update_schema(schema):
    data = request.get_json()
    existing_schema = mongo.db.documents.find_one({'_id': schema})
    if existing_schema:
        mongo.db.documents.update_one({''})
        return success_response(200, "Document Schema Created")
    else:
        return success_response(200, "Document not created")


# get schema/steps list
@workflow_blueprint.route('/schema', methods=['GET'])
def get_schema():
    code, message, result, pagination = get_schema_list()
    if result:
        return success_response(200, result, message, pagination)
    else:
        return success_response(200, message)


# get schema/steps details
@workflow_blueprint.route('/schema/<schema_id>', methods=['GET'])
def schema_details(schema_id):
    try:
        code, message, result = detail_schema(schema_id)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


# delete schema/steps
@workflow_blueprint.route('/schema/<id>', methods=["DELETE"])
def schema_delete(id):
    try:
        code, message, result = delete_schema(id)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, "Device not registered")
    except Exception as e:
        return error_response(400, str(e))


# create workflow instance
@workflow_blueprint.route('/workflow/<workflow>/step/<step>', methods=['POST'])
@validate_user
def create_workflow_instance(current_user, token, workflow, step):
    try:
        data = request.get_json()
        code, message, result = add_workflow_instance(data, workflow, step, token)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


# update workflow instance
@workflow_blueprint.route('/workflow/<workflow>/step/<step>', methods=['PUT'])
@validate_user
def workflow_instance_update(current_user, token, workflow, step):
    try:
        action_name = request.args.get('action_name')
        data = request.get_json()
        code, message, result = update_workflow_instance(data, action_name, workflow, step)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


# Get Event/MICE list
@workflow_blueprint.route('/workflow_instance/<workflow_id>', methods=["GET"])
@validate_user
def get_workflow_instance_list(current_user, token, workflow_id):
    """
    Get workflow_instance list
    :return: access and refresh token

    """
    try:
        event_id = request.args.get('event_id', None)
        code, message, result, pagination = workflow_instance_list(workflow_id, event_id)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


# Get Event/MICE Details
@workflow_blueprint.route('/workflow_instance/detail/<id>', methods=["GET"])
@validate_user
def get_events_details(current_user, token, id):
    """
    Get events/MICE list
    :return: access and refresh token

    """
    try:
        code, message, result = workflow_instance_details(id)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))
