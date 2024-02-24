import json
import os
import re
from functools import wraps
import requests
from flask import request

from app import config, mongo
import jwt

from bson.objectid import ObjectId
from app.utils.response import success_response
def validate_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        path = request.path
        path = path.split('/api/v1')[1]
        pattern = r"/workflow/([^/]+)/step/([^/]+)"
        match = re.match(pattern, path)
        # Check if there is a match
        if match:
            # Extract the values from the matched groups
            workflow_id = match.group(1)
            step_name = match.group(2)
            existing_workflow = mongo.db.workflow.find_one(
                {
                    "_id": ObjectId(workflow_id),
                    # "steps.document_schema": ObjectId(step_id),
                    "steps.name": step_name
                },
                {
                    "steps.$": 1
                }
            )
            allowed_roles = existing_workflow['steps'][0]['role']
        else:
            allowed_roles = ['initiator','employee','admin']
        payload = {}
        payload_json = json.dumps(payload)
        jwt_token = request.headers.get('x-access-token')
        url = os.environ.get('USER_AUTH_URL')
        headers = {'x-access-token': jwt_token, 'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload_json)
        # Print or inspect the response content
        if response.status_code == 200:
            current_user = response.json()
            if current_user['data']['role'] in allowed_roles:
                return fn(current_user, jwt_token, *args, **kwargs)
            else:
                return success_response(401, {}, "Access Denied !!!")
        else:
            return success_response(401, {}, "Unauthorized")
    return wrapper