from urllib.parse import urlparse

import boto3
import botocore
import os
from botocore.exceptions import NoCredentialsError

from app import mongo
from bson.objectid import ObjectId
from app.config import AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_BUCKET_NAME


def upload_file_to_s3(file, bucket_name, access_key, secret_key, region):
    # Connect to S3 bucket
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)

    try:
        # Upload file to S3 bucket
        s3.upload_fileobj(file, bucket_name, file.filename)
        pre_signed_url = s3.generate_presigned_url('get_object',
                                                   Params={'Bucket': bucket_name, 'Key': file.filename},
                                                   ExpiresIn=3600)
        # Generate the public URL of the uploaded file
        # file_url=f'https://{bucket_name}.s3.{region}.amazonaws.com/{file.filename}'
        return pre_signed_url

    except NoCredentialsError:
        return 'AWS credentials not found'

    except Exception as e:
        return str(e)


def download_file_from_s3(bucket_name, object_key, access_key, secret_key, region):

    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

    try:
        # Parse the object URL to get the path
        parsed_url = urlparse(object_key)
        object_key = parsed_url.path.lstrip('/')

        # Full file path including the desired file name
        local_file_path = os.getcwd()+'/'+object_key

        # Download the file
        s3.download_file(bucket_name, object_key, local_file_path)
        print(f"File downloaded successfully to {local_file_path}")
        return True

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f"The specified key {object_key} does not exist in the bucket {bucket_name}")
        else:
            print(f"Error downloading file from S3: {str(e)}")

        return False


def upload_aws_bucket(file, bucket_name):
    try:
        client = boto3.client('s3',
                              region_name=AWS_REGION,
                              aws_access_key_id=AWS_ACCESS_KEY,
                              aws_secret_access_key=AWS_SECRET_KEY
                              )

        client.put_object(Bucket=bucket_name, Key=file.filename, Body=file, ACL='public-read'
                          ,
                          ContentType=file.content_type)  # ACL='public-read',  ContentType=first_file_name.content_type

        s3_path = f"https://{bucket_name}.s3.amazonaws.com/{file.filename}"

        file_size = file.tell()
        print(file_size)
        attachment_type = file.content_type
        print(attachment_type.split('/')[0])
        file_type = attachment_type.split('/')[0]
        return s3_path, file_type, file_size
    except NoCredentialsError:
        return 'AWS credentials not found'
    except Exception as e:
        return str(e)


def delete_file_from_s3(media_id):
    try:
        existing_media = mongo.db.document_files.find_one({'_id': ObjectId(media_id)})
        if existing_media:
            delete_media = mongo.db.document_files.delete_one({'_id': ObjectId(media_id)})

            print("Media path ==>", existing_media['path'])
            deleted_media = existing_media['path']

            client = boto3.client('s3',
                                  region_name=AWS_REGION,
                                  aws_access_key_id=AWS_ACCESS_KEY,
                                  aws_secret_access_key=AWS_SECRET_KEY
                                  )
            object_url = existing_media['path']
            object_key = object_url.replace(f'https://{AWS_BUCKET_NAME}.s3.amazonaws.com/', '')

            client.delete_object(Bucket=AWS_BUCKET_NAME, Key=object_key)
            return 200, deleted_media, {}
        else:
            return 400, 'No media found !!!', {}
    except NoCredentialsError:
        return 'AWS credentials not found'
    except Exception as e:
        return str(e)

