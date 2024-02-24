from flask import jsonify, request
from app import mongo
from jsonschema import validate, exceptions, ValidationError
import json
from bson.objectid import ObjectId
from app.utils.helpers import schema_validator
import os
from app.utils.api_call import make_api_call


def role(data):
    role_name = data.get('role_name')
    status = data.get('status')
    name = data.get('name')
    permissions = data.get('permissions')
    current_file_path = os.path.abspath(__file__)
    parent_dir_path = os.path.dirname(current_file_path)
    role_model_path = os.path.join(parent_dir_path, "../models/role_model.json")
    is_validated = schema_validator(data, role_model_path)
    if not is_validated:
        if role_name and status and name and permissions:
            url = os.environ.get('MASTER_DATA_URL')
            response = make_api_call(url=url, method="GET")
            if response.get('data'):
                roles_in_response = response['data'][0].get('role', [])
                if role_name not in roles_in_response:
                    return 400, 'Invalid Role Name', {}
            if data['permissions']:
                print("ttttt",data['permissions'])
                permission_list = []
                for group in permissions:
                    roles_cursor = mongo.db.permissions.find(
                        {'group': group},
                        {'_id': 0, 'name': 0, 'dependency': 0, 'description': 0, 'group': 0, 'sorting_position': 0}
                    )
                    # Convert the cursor to a list to avoid exhausting it
                    roles = list(roles_cursor)
                    roles_count = len(roles)
                    print("hhhhh",roles_count)
                    if roles_count > 0:
                        for role_data in roles:
                            permission_list.append(role_data)
                    else:
                        # return 400, 'Invalid role', {}
                        pass
                existing_document = mongo.db.role_permission.find_one({'role_name': role_name})
                if existing_document:
                    mongo.db.role_permission.update_one({'_id': existing_document['_id']},
                                                        {'$set': {'permissions': permission_list, 'status': status,
                                                                  'name': name}})
                else:
                    # Insert the role into the MongoDB collection
                    new_role = {}
                    new_role['role_name'] = role_name
                    new_role['name'] = name
                    new_role['status'] = status
                    new_role['permissions'] = permission_list
                    mongo.db.role_permission.insert_one(new_role)
                return 200, 'Role added successfully', {}
            else:
                return 400, 'Invalid data', {}
        else:
            return 400, 'Invalid inputs', {}
    else:
        return 400, 'Validation failed', {}


def role_permission_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # pagination
    total_count = mongo.db.role_permission.count_documents({})
    pages = int(total_count / per_page) + (total_count % per_page > 0)
    start = (page - 1) * per_page

    users = mongo.db.role_permission.find({"status": "active"},
                                          {"_id": 1, "role_name": 1, "status": 1, "permissions": 1}).skip(
        start).limit(per_page)
    user_list = []
    if users:
        for user in users:
            user['_id'] = str(user['_id'])
            user_list.append(user)

        pagination = {
            'total': total_count,
            'pages': pages,
            'page': page,
            'per_page': per_page
        }
        if len(user_list) > 0:
            return 200, "Role List", user_list, pagination
        else:
            return 400, "No Data", {}, {}
    else:
        return 400, "No Data", {}, {}


def get_role_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # pagination
    total_count = mongo.db.role_permission.count_documents({})
    pages = int(total_count / per_page) + (total_count % per_page > 0)
    start = (page - 1) * per_page

    users = mongo.db.role_permission.find({"status": "active"},
                                          {"_id": 1, "role_name": 1, "status": 1, "name": 1}).skip(
        start).limit(per_page)
    user_list = []
    if users:
        for user in users:
            user['_id'] = str(user['_id'])
            user_list.append(user)

        pagination = {
            'total': total_count,
            'pages': pages,
            'page': page,
            'per_page': per_page
        }
        return 200, "Role List", user_list, pagination
    else:
        return 400, "No Data", {}


# def get_permission_list():
#     groups = mongo.db.permissions.distinct("group")
#     print("ttttttt", groups)
#     if groups:
#         for i in groups:
#             permissions_assigned = mongo.db.permissions.find({'group': i})
#             print("===========================", permissions_assigned)
#             if permissions_assigned:
#                 for j in permissions_assigned:
#                     print("llllllllllllll", j)
#
#         return 200, "Permission List", groups
#     else:
#         return 400, "No Data", {}

def get_permission_list():
    group_permissions = {}
    groups = mongo.db.permissions.distinct("group")
    if groups:
        for group in groups:
            permissions_assigned = mongo.db.permissions.find({'group': group})
            if permissions_assigned:
                permissions_list = []
                for permission in permissions_assigned:
                    permission_info = {
                        'method': permission['method'],
                        'endpoint': permission['endpoint'],
                        'key': permission['key'],
                        'name': permission['name'],
                    }
                    permissions_list.append(permission_info)
                group_permissions[group] = permissions_list
        return 200, "Permission List", group_permissions
    else:
        return 400, "No Data", {}


def permissions(data):
    # Check if the permission key is already in the database
    existing_permission = mongo.db.permissions.find_one({'key': data.get('key')})
    if existing_permission:
        return 400, 'Duplicate permission key', {}
    current_file_path = os.path.abspath(__file__)
    parent_dir_path = os.path.dirname(current_file_path)
    role_model_path = os.path.join(parent_dir_path, "../models/permissions.json")
    is_validated = schema_validator(data, role_model_path)
    if not is_validated:
        # Insert the role into the MongoDB collection
        permissions_id = mongo.db.permissions.insert_one(data).inserted_id
        return 200, 'Permission added successfully', {'permissions_id': str(permissions_id)}
    else:
        return 400, 'Validation failed', {}
