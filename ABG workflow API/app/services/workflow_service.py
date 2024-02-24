import os
from datetime import datetime, timedelta
from openpyxl import load_workbook
import pymongo
import requests

from app.config import ORG_BASE_URL, AWS_BUCKET_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION
from app.services.fileUpload_service import employee_bulk_upload
from app.utils.api_call import make_api_call
from app.utils.jwt import get_jwt_token, get_jwt
from app.utils.general_utils import generate_session_code, update_session, generate_request_code
from flask import g, request, jsonify
import jwt
from app import mongo, mail, bcrypt
from app.utils.notifications import send_notification, create_notification_data
from app.utils.response import error_response, success_response
from app.utils.helpers import schema_validator
from bson.objectid import ObjectId
import json
import random
import string
from flask_mail import Mail, Message
from openpyxl import load_workbook, Workbook
# import pandas as pd
import math

from app.utils.s3 import download_file_from_s3


def create_workflow(data):
    if data:
        is_validated = schema_validator(data, 'workflow_model.json')
        if not is_validated:
            for step in data['steps']:
                step['document_schema'] = ObjectId(step['document_schema'])
            result = mongo.db.workflow.insert_one(data)
            if result.inserted_id:
                return 200, "Workflow Created", {}
            else:
                return 200, "Validation Failed"
        else:
            return 200, "Validation Failed"


def update_workflow(id, data):
    existing_workflow = mongo.db.workflow.find_one({'_id': id})
    if existing_workflow:
        is_validated = schema_validator(data, 'workflow_model.json')
        if not is_validated:
            result = mongo.db.workflow.update_one(data)
            # inserted_id = str(result.inserted_id)
            return 200, "Workflow Details Updated", {}
        else:
            return 200, "Validation Failed", {}
    else:
        return 200, "Data not found", {}


def list_workflow():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # pagination
    total_count = mongo.db.workflow.count_documents({})
    pages = int(total_count / per_page) + (total_count % per_page > 0)
    start = (page - 1) * per_page

    workflow_list = mongo.db.workflow.find({}).skip(start).limit(per_page)

    if workflow_list:
        result = []
        for workflow in workflow_list:
            workflow['_id'] = str(workflow['_id'])
            if workflow['steps']:
                for document in workflow['steps']:
                    document['document_schema'] = str(document['document_schema'])
            result.append(workflow)

        pagination = {
            'total': total_count,
            'pages': pages,
            'page': page,
            'per_page': per_page
        }
        return 200, 'Workflow list', result, pagination
    else:
        return 400, 'No data', {}


def detail_workflow(workflow):
    existing_workflow = mongo.db.workflow.find_one({'_id': ObjectId(workflow)})
    if existing_workflow:
        existing_workflow['_id'] = str(existing_workflow['_id'])
        for document in existing_workflow['steps']:
            document['document_schema'] = str(document['document_schema'])
        return 200, 'Workflow details', existing_workflow
    else:
        return 400, 'No data', {}


def delete_workflow(id, data):
    # Find the document to delete
    result = mongo.db.workflow.find_one_and_delete({'_id': id})

    # If the document was not found, return a 404 error
    if not result:
        return 200, 'Data not found', {}

    # Return a success message
    return 200, 'Document deleted successfully', {}


def get_schema_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # pagination
    total_count = mongo.db.workflow.count_documents({})
    pages = int(total_count / per_page) + (total_count % per_page > 0)
    start = (page - 1) * per_page
    schema_list = mongo.db.documents.find({}).skip(start).limit(per_page)
    if schema_list:
        result = []
        for schema in schema_list:
            # schema['_id'] = str(schema['_id'])
            result.append(schema)

        pagination = {
            'total': total_count,
            'pages': pages,
            'page': page,
            'per_page': per_page
        }
        return 200, 'Schema list', result, pagination
    else:
        return 400, 'No Schema found', {}


def detail_schema(schema_id):
    existing_schema = mongo.db.documents.find_one({'_id': ObjectId(schema_id)})
    if existing_schema:
        return 200, 'Schema Details', existing_schema
    else:
        return 400, 'No data found', {}


def delete_schema(id):
    # Find the document to delete
    result = mongo.db.documents.find_one_and_delete({'_id': ObjectId(id)})

    # If the document was not found, return a 404 error
    if not result:
        return 200, 'Data not found', {}

    # Return a success message
    return 200, 'Schema deleted successfully', {}


def add_workflow_instance(datas, workflow, step,token):
    # token = {'x-access-token': token}
    total_instance = len(datas['instance'])
    workflow_instance = []
    for data in datas['instance']:
        existing_workflow = mongo.db.workflow.find_one(
            {
                "_id": ObjectId(workflow),
                # "steps.document_schema": ObjectId(step_id),
                "steps.name": step
            },
            {
                "steps.$": 1
            }
        )
        if not existing_workflow:
            return 404, "Workflow or step not found", {}

        data['status'] = existing_workflow['steps'][0]['status']
        data['workflow_id'] = ObjectId(workflow)
        data['current_step'] = step
        # Check if auto transition is required
        if existing_workflow['steps'][0].get('auto_transition', False):
            auto_transition_to = existing_workflow['steps'][0].get('auto_transition_to', None)
            if auto_transition_to:
                next_step = mongo.db.workflow.find_one(
                    {
                        "_id": ObjectId(workflow),
                        # "steps.document_schema": ObjectId(step_id),
                        "steps.name": auto_transition_to
                    },
                    {
                        "steps.$": 1
                    }
                )
                data['current_step'] = auto_transition_to
                data['status'] = next_step['steps'][0].get('status', None)
        create_instance = mongo.db.workflow_instance.insert_one(data)
        if create_instance:
            # # downloading the file S3
            if data['type'] in ["event", "mice"]:
                if 'employee_file_path' in data and data['employee_file_path']:
                    object_key = data.get('employee_file_path', [{}])[0].get('path')
                    parts = object_key.split('/')
                    object_key = '/'.join(parts[3:])

                    file_data = download_file_from_s3(AWS_BUCKET_NAME, object_key, AWS_ACCESS_KEY, AWS_SECRET_KEY,
                                                      AWS_REGION)

                    # extract the data from file
                    code = employee_bulk_upload(create_instance.inserted_id, object_key, data['event_name'], token)

            workflow_instance.append(create_instance.inserted_id)
        else:
            return 400, "Something went wrong!"
    if len(workflow_instance) == total_instance:
        return 200, "Instance Created", {"workflow_instance_id": workflow_instance}
    else:
        return 400, "Something went wrong when creating instance"


def update_workflow_instance(datas, action_name, workflow, step):
    total_instance = len(datas['instance'])
    result = []
    for data in datas['instance']:

        workflow_instance_id = data["workflow_instance_id"]

        workflow_instance = mongo.db.workflow_instance.find_one(
            {"_id": ObjectId(workflow_instance_id), "workflow_id": ObjectId(workflow)}
        )

        if not workflow_instance:
            return 400, "Workflow instance not found for the specified event", {}

        current_step_name = workflow_instance.get("current_step")

        # Find the workflow definition
        existing_workflow = mongo.db.workflow.find_one(
            {"_id": ObjectId(workflow)}
        )

        if not existing_workflow:
            return 400, "Workflow not found", {}

        # Find the details of the current step in workflow
        current_step = next((s for s in existing_workflow.get("steps", []) if s["name"] == current_step_name), None)

        if not current_step:
            return 400, "Details for the current step not found", {}

        # Check if the specified action is allowed for the current step
        allowed_actions = [action["name"] for action in current_step.get("actions", [])]

        if action_name not in allowed_actions:
            return 400, "Invalid action for the current step", {}

        # Find the details of the next step based on the action
        next_step = next(
            (action for action in current_step["actions"] if action["name"] == action_name), None
        )
        if not next_step:
            return 400, "Details for the next step not found", {}

        # Fetch the details of the next step to get the status
        next_step_details = next(
            (s for s in existing_workflow.get("steps", []) if s["name"] == next_step.get("next_step", "")), None
        )
        if not next_step_details:
            # Check if the next step leads to another workflow
            next_workflow_id = next_step.get("next_workflow", None)
            if not next_workflow_id:
                return 400, "Details for the next step/workflow not found", {}
            else:
                return 400, "Workflow not found", {}
        data["current_step"] = next_step.get("next_step")
        data["status"] = next_step_details.get("status")
        data["workflow_id"] = ObjectId(data["workflow_id"])
        update_result = mongo.db.workflow_instance.update_one(
            {"_id": ObjectId(workflow_instance_id)}, {"$set": data}

        )
        if update_result.modified_count == 1:
            result.append(workflow_instance_id)
        else:
            return 400, "Something went wrong"
    if len(result) == total_instance:
        return 200, "Instance Updated", {"workflow_instance_id": result}
    else:
        return 400, "Something went wrong when updating instance"


def workflow_instance_list(workflow_id,event_id):
    workflow_type = request.args.get('workflow_type', None)
    if workflow_type and workflow_type not in ['image', 'event','review','mice']:
        return 400, 'Invalid type. It should be either event or mice', {}, {}
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    # pagination
    total_count = mongo.db.workflow_instance.count_documents({})
    pages = int(total_count / per_page) + (total_count % per_page > 0)
    start = (page - 1) * per_page
    workflow_instance = mongo.db.workflow_instance.find({"workflow_id": ObjectId(workflow_id), "type": workflow_type}).skip(
        start).limit(per_page)
    workflow_instance_list = []
    if workflow_instance:
        if workflow_type in ['event', 'mice']:
            for instance in workflow_instance:
                instance['_id'] = str(instance['_id'])
                image_count = mongo.db.workflow_instance.count_documents(
                    {"event_id": instance['_id'], "status": 'approved','type': 'image'})
                reviews = mongo.db.workflow_instance.find(
                    {"event_id": instance['_id'], "status": 'approved','type':'review'})
                # Calculate average rating from reviews
                total_rating = 0
                review_count = 0
                for review in reviews:
                    if 'rating' in review:
                        total_rating += review['rating']
                        review_count += 1

                avg_rating = total_rating / review_count if review_count > 0 else 0
                instance['image_count'] = image_count
                instance['avg_rating'] = avg_rating
                if image_count:
                    instance['image_count'] = image_count
                workflow_instance_list.append(instance)

            pagination = {
                'total': total_count,
                'pages': pages,
                'page': page,
                'per_page': per_page
            }
            return 200, "workflow instance list", workflow_instance_list, pagination
        elif workflow_type in ['image','review'] and event_id:
            workflow_instance = mongo.db.workflow_instance.find(
                {"workflow_id": ObjectId(workflow_id), "type": workflow_type,"event_id":str(event_id)}).skip(
                start).limit(per_page)
            if workflow_instance:
                for data in workflow_instance:
                    print("data",data)
                    data['_id'] = str(data['_id'])
                    workflow_instance_list.append(data)
                pagination = {
                    'total': total_count,
                    'pages': pages,
                    'page': page,
                    'per_page': per_page
                }
                return 200, "workflow instance list", workflow_instance_list, pagination
        else:
            return 400, "No Data found", {}, {}
    else:
        return 400, "No Data", {}, {}


def workflow_instance_details(workflow_instance_id):
    instance = mongo.db.workflow_instance.find_one({'_id': ObjectId(workflow_instance_id)})
    if instance:
        instance['_id'] = str(instance['_id'])

        return 200, "workflow instance Details", instance
    else:
        return 400, "Invalid instance id", {}