from flask import g, request
from app import mongo
from bson.objectid import ObjectId
from app.config import ORG_BASE_URL, AWS_BUCKET_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION
from app.services.fileUpload_service import employee_bulk_upload
from app.utils.s3 import download_file_from_s3


def get_images(added_by, event_id):
    lis = []
    approved_image_of_event = mongo.db.workflow_instance.find(
        {'event_id': event_id, 'added_by': added_by, 'status': 'approved'},
        {'path': 1, '_id': 1})
    if approved_image_of_event:

        for image in approved_image_of_event:
            lis.append(image)

        return (lis)
    else:
        return 400, "image not found", {}


def add_wallet(payload):
    lis = []

    upload_wallet_result = mongo.db.wallet.insert_one({
        "type": payload["type"],
        "path": payload["path"],
        "added_by": payload["added_by"]
    })

    if upload_wallet_result.acknowledged:
        return "Uploaded successfully"
    else:
        return 400, "Insertion failed", {}


def get_wallet(user_id):
    lis = []

    wallet = mongo.db.wallet.find({'added_by': user_id})

    if wallet:
        for data in wallet:
            lis.append(data)
        return lis

    else:
        return 400, "Insertion failed", {}


def event_names(user_id):
    lis = []
    user_id = ObjectId(user_id)
    names = mongo.db.workflow_instance.find({"employee.user_id": ObjectId('65c5bd362b1e46f1049c4d81')}, {'business': 1})
    if names:
        for name in names:
            lis.append(name)
        return lis
    else:
        return 400, "Insertion failed", {}


def post_travel_partners():
    try:
        if all(key in request.args for key in ['type']):
            type = request.args.get('type')
            data = request.get_json()
            if type == "event":
                create_instance = mongo.db.event_travelpartners.insert_one(data)
            elif type == "mice":
                create_instance = mongo.db.mice_travelpartners.insert_one(data)
            else:
                return 400, "type not found", {}
            if create_instance:
                return 200, "Successfully inserted", {}
            else:
                return 400, "Something went wrong!", {}
        else:
            return 400, "type not found"
    except Exception as e:
        return 400, str(e), {}


def fetch_travel_partners():
    try:
        if all(key in request.args for key in ['type']):
            type = request.args.get('type')
            if type in ['event', 'mice']:
                instances = list(mongo.db.travelpartners.find({'type': type}))
            else:
                return 400, "type incorrect", {}
            if instances:
                for instance in instances:
                    instance['_id'] = str(instance['_id'])
                return 200, "Travel partner Details", instances
            else:
                return 400, "No data found", {}
        else:
            return 400, "Type not found", {}
    except Exception as e:
        return 400, str(e), {}


def fetch_images_reviews():
    try:
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        type = request.args.get('type')
        event_type = request.args.get('event_type')

        allowed_statuses = ['IMAGES_APPROVED', 'IMAGES_REJECTED', 'IMAGE_APPROVAL', None, 'REVIEW_APPROVAL',
                            'REVIEWS_REJECTED', 'REVIEWS_APPROVED']
        allowed_types = ['image', 'review']

        if type is None:
            return 400, "Type not found", {}
        if type not in allowed_types:
            return 400, f"Type allowed: {allowed_types}", {}

        if event_type is None:
            return 400, "Event type not found", {}

        if status not in allowed_statuses:
            return 400, f"Status invalid, allowed statuses: {allowed_statuses}", {}

        query = {"type": type}
        if user_id:
            query["added_by"] = user_id
        if status:
            query["current_step"] = status

        instances = list(mongo.db.workflow_instance.find(query))

        if instances:
            event_based_items = {}
            for instance in instances:
                event_id = instance['event_id']
                event = mongo.db.workflow_instance.find_one({"_id": ObjectId(event_id)})
                if event and event['type'] == event_type:
                    if event_id not in event_based_items:
                        event_based_items[event_id] = {
                            "event_id": event_id,
                            "event_type": event['type'],
                            "event_name": event['event_name'],
                            "event_based_datas": []
                        }
                    event_based_items[event_id]["event_based_datas"].append(instance)

            event_details = list(event_based_items.values())
            return 200, "Image/Review details based on events", {"image_review_details": event_details}
        else:
            return 400, "No data found", {}

    except Exception as e:
        return 400, str(e), {}


def add_uploaded_image_info():
    try:
        data = request.get_json()
        create_instance = mongo.db.policies_documents.insert_one(data)
        if create_instance:
            return 200, "Successfully inserted", {}
        else:
            return 400, "Something went wrong!", {}
    except Exception as e:
        return 400, str(e), {}


def fetch_policies_documents():
    try:
        document_name = request.args.get('document_name')
        query = {} if document_name is None else {"document_name": document_name}
        instances = list(mongo.db.policies_documents.find(query))
        if instances:
            for instance in instances:
                instance['_id'] = str(instance['_id'])
            return 200, "policies_documents Details", instances
        else:
            return 400, "No data found", {}

    except Exception as e:
        return 400, str(e), {}


def review_details(current_user):
    try:
        event_id = request.args.get('event_id', None)
        result_data = []
        if current_user["data"]["role"] in ['employee', 'initiator']:
            query_1 = {"event_id": str(event_id), "type": "review", "added_by": current_user["data"]["_id"]}

            query_2 = {"event_id": str(event_id), "type": "review", "current_step": "REVIEW_APPROVED",
                       "added_by": {"$ne": current_user["data"]["_id"]}}

            workflow_instance_list_1 = list(mongo.db.workflow_instance.find(query_1))
            result_data.extend(workflow_instance_list_1)

            workflow_instance_list_2 = list(mongo.db.workflow_instance.find(query_2))
            result_data.extend(workflow_instance_list_2)
            return 200, "Review list", result_data

        elif current_user["data"]["role"] in ['admin']:

            query1 = {"event_id": str(event_id), "type": "review", "current_step": "REVIEW_APPROVAL"}
            query2 = {"event_id": str(event_id), "type": "review", "current_step": "REVIEW_APPROVED"}
            query3 = {"event_id": str(event_id), "type": "review", "current_step": "REVIEW_REJECTED"}

            workflow_instance_list_1 = list(mongo.db.workflow_instance.find(query1))
            result_data.extend(workflow_instance_list_1)

            workflow_instance_list_2 = list(mongo.db.workflow_instance.find(query2))
            result_data.extend(workflow_instance_list_2)

            workflow_instance_list_3 = list(mongo.db.workflow_instance.find(query3))
            result_data.extend(workflow_instance_list_3)
            return 200, "Review list", result_data

        else:
            return 400, 'user not found', {}

    except Exception as e:
        return 400, str(e), {}

def update_files(token):
    try:
        workflow_instance_id = request.args.get('workflow_instance_id', None)
        if workflow_instance_id is not None:
            data = request.get_json()

            update_result = mongo.db.workflow_instance.update_one(
                {"_id": ObjectId(workflow_instance_id)},
                {"$set": data},
                upsert=True  # Insert the document if it does not exist
            )
            event_details = mongo.db.workflow_instance.find({'_id':ObjectId(workflow_instance_id)})
            for detail in event_details:
                event_name = detail['event_name']
            if 'employee_file_path' in data and data['employee_file_path']:
                object_key = data.get('employee_file_path', [{}])[0].get('path')
                parts = object_key.split('/')
                object_key = '/'.join(parts[3:])

                file_data = download_file_from_s3(AWS_BUCKET_NAME, object_key, AWS_ACCESS_KEY, AWS_SECRET_KEY,
                                                  AWS_REGION)

                code = employee_bulk_upload(workflow_instance_id, object_key, event_name, token)
            if update_result.acknowledged:
                return 200, "Files added to workflow_instance successfully", {}
            else:
                return 400, 'work flow instance not found', {}

        else:
            return 400, 'work flow instance not found', {}

    except Exception as e:
        return 400, str(e), {}
