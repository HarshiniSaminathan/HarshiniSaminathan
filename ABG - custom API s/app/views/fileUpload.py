from bson import ObjectId
from flask import Blueprint, request,send_file
import os
from app.middleware import validate_user
from app.utils.response import success_response,error_response
import json
from datetime import datetime
from app import mongo, config

from app.utils.s3 import upload_file_to_s3, upload_aws_bucket, delete_file_from_s3
from app.utils.notifications import get_notification_list, mark_all_read

file_upload_blueprint = Blueprint('file_upload', __name__, url_prefix='/api/v1')


@file_upload_blueprint.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        file_name = file.filename

        # Set your S3 bucket details and AWS credentials
        bucket_name = os.environ.get('AWS_BUCKET_NAME')
        if file:
            # Upload the file to S3 and get the file URL
            s3_path, file_type, file_size = upload_aws_bucket(file, bucket_name)
            if file_size and file_type and s3_path:
                file_extension = file_name.split('.')[-1]
                data = {
                    "path": s3_path,
                    "file_size": file_size,
                    "file_type": file_extension

                }
                document_id = mongo.db.document_files.insert_one(data).inserted_id
                result = {'path': str(s3_path), 'media_id': str(document_id), 'file_size': file_size,
                          'file_type': file_type, 'file_extension': file_extension}
                response_data = {'message': 'File uploaded successfully', 'data': result}
                return response_data, 200
            else:
                return 400, 'Invalid Path or FileType or FileSize', {}
        else:
            return 400, 'No File Found', {}
    except Exception as e:
        return error_response(400, str(e))
    

@file_upload_blueprint.route('/upload_multiple_file', methods=['POST'])
def upload_multiple_file():
    try:
        user_id = request.form['added_by']
        files = request.files.getlist('file')
        list_of_path=[]
        for data in files:
            file_name = data.filename

            # Set your S3 bucket details and AWS credentials
            bucket_name = os.environ.get('AWS_BUCKET_NAME')
            if files:
                lis=[]
                # Upload the file to S3 and get the file URL
                s3_path, file_type, file_size = upload_aws_bucket(data, bucket_name)
                if file_size and file_type and s3_path:
                    file_extension = file_name.split('.')[-1]
                    list_of_path.append(s3_path)
            else:
                return 400, 'No File Found', {}
            
        data = {
            "path":list_of_path,
            "added_by":user_id
        }
        document = mongo.db.wallet.insert_one(data)
        if document.acknowledged :
            response_data = {'message': 'File uploaded successfully', 'data': data}
            return success_response(200,data,"success",pagination=0)
        return 400, 'failed to add in db'
    except Exception as e:
        return error_response(400, str(e)) 
