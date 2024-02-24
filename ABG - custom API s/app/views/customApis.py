from bson import ObjectId
from flask import Blueprint, request, send_file
import os
from app.middleware import validate_user
from app.services.customApis_Service import get_images, add_wallet, get_wallet, event_names, post_travel_partners, \
    fetch_travel_partners, fetch_images_reviews, add_uploaded_image_info, fetch_policies_documents, review_details, \
    update_files
from app.utils.response import success_response, error_response

import traceback
import sys

customApis_blueprint = Blueprint('customApis', __name__, url_prefix='/api/v1')


@customApis_blueprint.route('/getUserApprovedImages', methods=["GET"])
def workflow_list():
    """
    get all approved image of current user

    """
    try:
        user_id = request.args.get('added_by')
        event_id = request.args.get('event_id')

        get_image = get_images(user_id, event_id)

        if get_image:
            return success_response(200, get_image, "success", pagination=0)
        # else:
        #     return error_response(400,"Data Not found")
    except Exception as e:
        print("error", e)
        return error_response(400, str(e))


@customApis_blueprint.route('/uploadWallet', methods=["POST"])
@validate_user(['employee', 'initiator'])
def uploadWallet(current_user, token):
    """
    get all approved image of current user

    """
    try:
        payload = request.get_json()

        if "type" not in payload or payload['type'] == '':
            return error_response(400, "type missing in payload")

        if "path" not in payload or payload['path'] == '':
            return error_response(400, "path missing in payload")

        if "added_by" not in payload or payload['added_by'] == '':
            return error_response(400, "added_by key missing in payload")

        wallet = add_wallet(payload)

        if wallet:
            return success_response(200, "data added successfully", "success", pagination=0)
        # else:
        #     return error_response(400,"Data Not found")
    except Exception as e:
        print("error", e)
        errors = traceback.print_exc(file=sys.stdout)
        return error_response(400, str(e))


@customApis_blueprint.route('/getWallet', methods=["GET"])
@validate_user(['employee', 'initiator'])
def getWallet(current_user, token):
    """
    get all approved image of current user

    """
    try:
        user_id = request.args.get('added_by')

        wallet = get_wallet(user_id)
        if wallet:
            return success_response(200, wallet, "success", pagination=0)
        # else:
        #     return error_response(400,"Data Not found")
    except Exception as e:
        print("error", e)
        return error_response(400, str(e))


@customApis_blueprint.route('/getEventNames', methods=["GET"])
def get_event_names():
    """
    get all approved image of current user

    """
    try:
        user_id = request.args.get('added_by')

        names = event_names(user_id)
        if names:
            return success_response(200, names, "success", pagination=0)
        # else:
        #     return error_response(400,"Data Not found")
    except Exception as e:
        print("error", e)
        return error_response(400, str(e))



@customApis_blueprint.route("/add_travel_partners", methods=['POST'])
def add_travel_partners():
    try:
        code, message, result = post_travel_partners()
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@customApis_blueprint.route("get_travel_partners", methods=['GET'])
@validate_user(['employee', 'initiator'])
def get_travel_partners(current_user, token):
    try:
        code, message, result = fetch_travel_partners()
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@customApis_blueprint.route("get_images_reviews", methods=['GET'])
@validate_user(['employee', 'initiator'])
def get_images_reviews(current_user, token):
    try:
        code, message, result = fetch_images_reviews()
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@customApis_blueprint.route("post_uploaded_document_info", methods=['POST'])
def post_uploaded_document_info():
    try:
        code, message, result = add_uploaded_image_info()
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@customApis_blueprint.route("get_policies_documents", methods=['GET'])
@validate_user(['employee', 'initiator'])
def get_policies_documents(current_user, token):
    try:
        code, message, result = fetch_policies_documents()
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@customApis_blueprint.route("get_review_details", methods=['GET'])
@validate_user(['employee', 'initiator', 'admin'])
def get_review_details(current_user, token):
    try:
        code, message, result = review_details(current_user)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))


@customApis_blueprint.route("update_files_workflow_instance", methods=['PUT'])
@validate_user(['employee', 'initiator', 'admin'])
def update_files_workflow_instance(current_user, token):
    try:
        code, message, result = update_files(token)
        if code == 200:
            return success_response(200, result, message)
        else:
            return error_response(400, message)
    except Exception as e:
        return error_response(400, str(e))
