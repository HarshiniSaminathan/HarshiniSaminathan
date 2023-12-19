import base64
import json
import os
import hashlib
import uuid
from functools import wraps

from flask import request, session
import jwt
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

from app.controller.userController import (check_email_existence, insert_user, check_login, check_username_existence,
                                           check_account_Type, \
                                           check_email_For_Username, add_profile, updateSessionCode,
                                           update_Message_Status,
                                           check_emailhas_sessionCode, block_friend, unblock_friend, Get_block_list,
                                           Get_Profile_Info_ByUsername, likepost,
                                           unlikepost, responding_For_Resquest, Get_Particular_friends_post,
                                           unfollow_friend, Get_Profile_Info, List_followers, postMessages,
                                           Get_friends_profile, Get_friends_post, List_following, deleteSession,
                                           addPost, delete_Post, check_post_exists, status_for_request,
                                           request_to_follow, check_postid, search_username, save_comments,
                                           save_replycomments, deletecomment, check_delete_access, deleteMessage,
                                           Get_entire_messages, check_for_hashtags, get_posts, update_password)
from app.models.likeModel import Like

from app.response import failure_response, success_response
from config import SECRET_KEY



def generate_session_code(user_info):
    user_info_str = str(user_info)
    hash_object = hashlib.sha256(user_info_str.encode())
    session_code = hash_object.hexdigest()
    return session_code

def generate_jwt_token(user_info):
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    payload = {
        'EmailId': user_info['EmailId'],
        'Role': user_info['Role'],
        'exp': expiration_time,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def generate_refresh_token(user_info):
    expiration_time = datetime.utcnow() + timedelta(hours=24)
    payload = {
        'EmailId': user_info['EmailId'],
        'Role': user_info['Role'],
        'exp': expiration_time,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def user_Sign_Up():
    try:
        data = request.get_json()
        required_fields = ['emailid', 'password', 'username', 'fullname','accountType']
        if required_fields:
            for field in required_fields:
                if field not in data or not data[field]:
                    return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
            emailid = data['emailid']
            password = data['password']
            username = data['username']
            fullname = data['fullname']
            accountType = data['accountType']
            role = "USER"
            status="INACTIVE"
            if not check_email_existence(emailid):
                if not check_username_existence(username):
                    insert_user(emailid, password, username, fullname, role, status,accountType)
                    return success_response('User Added Successfully')
                return failure_response(statuscode='409', content='UserName already exists')
            return failure_response(statuscode='409', content='Email id already exists')
        return failure_response(statuscode='409', content='required_fields Not found')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def login():
    try:
        data = request.get_json()
        required_fields = ['password', 'emailid']
        if required_fields:
            for field in required_fields:
                if field not in data or not data[field]:
                    return failure_response(statuscode='400', content=f'Missing or empty field: {field}')

            emailid = data['emailid']
            password = data['password']
            user = check_login(emailid, password)
            if user:
                role = user.role
                user_info = {'EmailId': emailid, 'Role': role}

                jwt_token = generate_jwt_token(user_info)
                jwt_token_str = jwt_token.decode('utf-8')

                refresh_token = generate_refresh_token(user_info)
                refresh_token_str = refresh_token.decode('utf-8')

                if jwt_token_str:
                    session_code = generate_session_code(user_info={'EmailId': emailid, 'Role': role})
                    print("session-CODE-LOGIN", session_code)
                    updateSessionCode(emailid, session_code)  # session Code add in the USER TABLE
                    return success_response({"data": role, "token": jwt_token_str, "Refresh-Token":refresh_token_str})
                else:
                    return failure_response(statuscode='400', content='User Invalid')
            else:
                return failure_response(statuscode='400', content='Invalid email or password')
        return failure_response(statuscode='409', content='required_fields Not found')

    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def log_Out():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                email = payload.get('EmailId')
                Role = payload.get('Role')
                session_code = generate_session_code(user_info={'EmailId': email, 'Role': Role})
                print("session-CODE-LOGOUT", session_code)
                if email:
                    if check_emailhas_sessionCode(email,session_code):
                        deleteSession(email)    # session Code delete in the USER TABLE
                        return success_response({"message": "Logout successful"})
                    else:
                        return failure_response(statuscode='401', content='Invalid session Code')
            except jwt.ExpiredSignatureError:
                return failure_response(statuscode='401', content='Token has expired')
            except jwt.InvalidTokenError:
                return failure_response(statuscode='401', content='Invalid token')
        return failure_response(statuscode='400', content='Token is missing or invalid')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def token_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            refresh_token = request.headers.get('Refresh-Token')  # Include a separate header for refresh token

            if not token or not refresh_token:
                return failure_response(statuscode='401', content='Token or Refresh-Token is missing')

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                EmailId = payload['EmailId']
                role = payload['Role']
                session_code = generate_session_code(user_info={'EmailId': EmailId, 'Role': role})
                print("session-CODE-API-VERIFY", session_code)
                if role not in allowed_roles:
                    return failure_response(statuscode='403', content=f'Access restricted. User is not authorized')

                if not check_emailhas_sessionCode(EmailId, session_code):
                    return failure_response(statuscode='401', content='Token has been invalidated (logged out)')

            except jwt.ExpiredSignatureError:
                try:
                    refresh_payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])

                    expiration_time = datetime.utcnow() + timedelta(hours=1)
                    new_access_token = generate_jwt_token({
                        'EmailId': refresh_payload['EmailId'],
                        'Role': refresh_payload['Role'],
                        'exp':expiration_time
                    }).decode('utf-8')

                    return success_response({"Access_token": new_access_token})
                except jwt.ExpiredSignatureError:
                    return failure_response(statuscode='401', content='Refresh token has expired')
                except jwt.InvalidTokenError:
                    return failure_response(statuscode='401', content='Invalid refresh token')

            except jwt.InvalidTokenError:
                return failure_response(statuscode='401', content='Invalid token')

            return func(*args, **kwargs)

        return wrapper

    return decorator

def addProfile():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                from run import UPLOAD_FOLDER
                file = request.files['file']
                form_data = request.form.get('data')
                try:
                    data = json.loads(form_data)
                except json.JSONDecodeError:
                    return failure_response(statuscode='400', content='Invalid JSON data')
                profileName = data['profileName']
                Bio = data['Bio']
                if check_email_For_Username(emailid):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    add_profile(emailid,filename,profileName,Bio)
                    return success_response("Profile Added successfully")
                return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')

    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

from PIL import Image, ImageOps, ExifTags
def rotate_image(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif_data = dict(image._getexif().items())
        print(exif_data[orientation])

        if exif_data[orientation] == 3 :
            image = image.rotate(180, expand=True)

        elif exif_data[orientation] == 6 :
            image = image.rotate(270, expand=True)

        elif exif_data[orientation] == 8 :
            image = image.rotate(90, expand=True)

    except (AttributeError, KeyError, IndexError):
        pass
    return image

def add_post():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                file = request.files['file']
                form_data = request.form.get('data')
                try:
                    data = json.loads(form_data)
                except json.JSONDecodeError:
                    return failure_response(statuscode='400', content='Invalid JSON data')

                postType = data['postType']
                caption = data['caption']
                tagUsername = data['tagUsername']
                status = 'INACTIVE'

                if check_email_For_Username(emailid):
                    for user in tagUsername:
                        if not check_username_existence(user):
                            return failure_response(statuscode='409', content=f'TagUserName:"{user}" does not exist/INACTIVE')

                    unique_key = str(uuid.uuid4())
                    filename = secure_filename(file.filename)
                    file_extension = os.path.splitext(filename)[1]
                    unique_filename = f"{unique_key}{file_extension}"
                    from run import UPLOAD_FOLDER
                    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                    file.save(file_path)
                    image = Image.open(file_path)
                    image = rotate_image(image)
                    max_width = 200
                    print(image.width)
                    if image.width > max_width:
                        aspect_ratio = max_width / float(image.width)
                        height = int(float(image.height) * float(aspect_ratio))
                        image = image.resize((max_width, height), Image.ANTIALIAS)

                    processed_image_path = os.path.join(UPLOAD_FOLDER, 'processed_' + unique_filename)
                    image.save(processed_image_path)

                    File_Name = unique_filename
                    addPost(emailid, postType, File_Name, caption, tagUsername, status)
                    return success_response("Post Added Successfully")
                return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exist/INACTIVE')

            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred, {e}.')

        return failure_response(statuscode='409', content='Token is missing')

    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred, {e}.')


def deletePost():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                data = request.get_json()
                required_fields = ['postid']
                if required_fields:
                    for field in required_fields:
                        if field not in data or not data[field]:
                            return failure_response(statuscode='400', content=f'Missing or empty field: {field}')

                    postid = data['postid']
                    if check_email_For_Username(emailid):
                        if check_post_exists(emailid,postid):
                            if delete_Post(emailid, postid):
                                return success_response("Post Deleted Successfully")
                            return failure_response(statuscode='409', content='Post Does Not Deleted')
                        return failure_response(statuscode='409', content='Post Does Not exists')
                    return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
                return failure_response(statuscode='409', content='required_fields Not found')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def requestForFollow():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                data=request.get_json()
                required_fields =['followerEmailid']
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                followerEmailid = data['followerEmailid']
                if check_email_For_Username(emailid):
                    if check_email_For_Username(followerEmailid):
                        if not check_account_Type(followerEmailid):  # If account Type == PRIVATE
                            if status_for_request(emailid,followerEmailid):
                                status = status_for_request(emailid, followerEmailid).status
                                return failure_response(statuscode='500', content=f'Already Request Sent,STATUS:{status}')
                            else:
                                status = 'PENDING'
                                request_to_follow(emailid,followerEmailid,status)
                                return success_response("Requested Successfully")
                        else:
                            status = 'ACCEPTED'
                            request_to_follow(emailid, followerEmailid,status)
                            return success_response("Following Successfully")
                    else:
                        return failure_response(statuscode='409', content=f'EmailId:{followerEmailid} does not exists/INACTIVE')
                else:
                    return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def responding_For_followRequest():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                data = request.get_json()
                required_fields = ['followerEmailid','statusToDone']
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')

                followerEmailid = data['followerEmailid']
                statusToDone = data['statusToDone']
                if check_email_For_Username(emailid):
                    if check_email_For_Username(followerEmailid):
                        status = status_for_request(emailid, followerEmailid).status
                        print(status)
                        if status != 'PENDING':
                            return failure_response(statuscode='500', content=f'Already Responsed Sent,STATUS:{status}')
                        else:
                            responding_For_Resquest(emailid, followerEmailid,statusToDone)
                            return success_response("Responded Successfully")
                    else:
                        return failure_response(statuscode='409', content=f'EmailId:{followerEmailid} does not exists/INACTIVE')
                else:
                    return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def unFollowFriend():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                data=request.get_json()
                required_fields = ['followerEmailid']
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                followerEmailid = data['followerEmailid']
                if check_email_For_Username(emailid):
                    if check_email_For_Username(followerEmailid):
                        status = status_for_request(emailid, followerEmailid).status
                        print(status)
                        if status=='ACCEPTED':
                            unfollow_friend(emailid,followerEmailid)
                            return success_response("Unfollow Successfully")
                        else:
                            return failure_response(statuscode='500', content=f'Already Not following,STATUS:{status}')
                    else:
                        return failure_response(statuscode='409', content=f'EmailId:{followerEmailid} does not exists/INACTIVE')

                else:
                    return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def veiw_Profile():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                page_header = request.headers.get('Page')
                per_page_header = request.headers.get('PerPage')
                if not page_header:
                    return failure_response(statuscode='401', content='page_header is missing')
                if not per_page_header:
                    return failure_response(statuscode='401', content='per_page_header is missing')
                if check_email_For_Username(emailid):
                    get_profile_info,total_following,total_followers,total_posts, total_pages = Get_Profile_Info(emailid,int(page_header), int(per_page_header))

                    return success_response({'data': get_profile_info ,'total_following':total_following,'total_followers':total_followers,'total_posts':total_posts,'Pagination': str(total_pages)})
                return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def following_List():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                page_header = request.headers.get('Page')
                per_page_header = request.headers.get('PerPage')
                if not page_header:
                    return failure_response(statuscode='401', content='page_header is missing')
                if not per_page_header:
                    return failure_response(statuscode='401', content='per_page_header is missing')

                if check_email_For_Username(emailid):
                    get_following_List, total_pages,total_following = List_following(emailid,int(page_header), int(per_page_header))

                    return success_response({'data': get_following_List ,'Pagination': str(total_pages),'Following_Count':str(total_following)})
                return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def Followers_List():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                page_header = request.headers.get('Page')
                per_page_header = request.headers.get('PerPage')
                if not page_header:
                    return failure_response(statuscode='401', content='page_header is missing')
                if not per_page_header:
                    return failure_response(statuscode='401', content='per_page_header is missing')
                if check_email_For_Username(emailid):
                    get_followers_List, total_pages,total_followers = List_followers(emailid,int(page_header), int(per_page_header))

                    return success_response({'data': get_followers_List ,'Pagination': str(total_pages),'Following_Count':str(total_followers)})
                return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def view_Friends_Profile():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                page_header = request.headers.get('Page')
                per_page_header = request.headers.get('PerPage')
                if not page_header:
                    return failure_response(statuscode='401', content='page_header is missing')
                if not per_page_header:
                    return failure_response(statuscode='401', content='per_page_header is missing')
                data = request.get_json()
                required_fields = ['followerEmailid']
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')

                followerEmailid = data['followerEmailid']
                if check_email_For_Username(emailid):
                    if check_email_For_Username(followerEmailid):
                        if not check_account_Type(followerEmailid): # NOT PUBLIC
                            if status_for_request(emailid, followerEmailid):
                                status = status_for_request(emailid, followerEmailid).status
                                print(status)
                                if status == 'ACCEPTED':
                                    profile_info, total_following, total_followers, total_posts = Get_friends_profile(
                                        emailid, followerEmailid, int(page_header),int(per_page_header))

                                    return success_response({'data': profile_info, 'total_following': total_following,
                                                             'total_followers': total_followers,'total_posts': total_posts})

                                return failure_response(statuscode='409', content=f'Not following')
                        profile_info, total_following,total_followers,total_posts,total_pages = Get_friends_profile(followerEmailid, int(page_header),
                                                                               int(per_page_header))
                        return success_response({'data': profile_info,'total_following':total_following,'total_followers':total_followers,'total_posts':total_posts,'Pagination':total_pages})
                    return failure_response(statuscode='409', content=f'EmailId:{followerEmailid} does not exists/INACTIVE')
                return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def view_Post():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                page_header = request.headers.get('Page')
                per_page_header = request.headers.get('PerPage')
                if not page_header:
                    return failure_response(statuscode='401', content='page_header is missing')
                if not per_page_header:
                    return failure_response(statuscode='401', content='per_page_header is missing')
                if check_email_For_Username(emailid):
                    get_friends_post, total_pages = Get_friends_post(emailid,int(page_header), int(per_page_header))
                    return success_response({'data': get_friends_post ,'Pagination': str(total_pages)})

                return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def view_Post_Of_ParticularFriend():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                page_header = request.headers.get('Page')
                per_page_header = request.headers.get('PerPage')
                if not page_header:
                    return failure_response(statuscode='401', content='page_header is missing')
                if not per_page_header:
                    return failure_response(statuscode='401', content='per_page_header is missing')
                data = request.get_json()
                required_fields = ['followingEmailid']
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                followingEmailid= data['followingEmailid']
                if check_email_For_Username(emailid):
                    if check_email_For_Username(followingEmailid):
                        if not check_account_Type(followingEmailid):
                            if status_for_request(emailid, followingEmailid):
                                status = status_for_request(emailid, followingEmailid).status
                                print(status)
                                if status == 'ACCEPTED':
                                    get_friends_post, total_pages,total_Post = Get_Particular_friends_post(emailid,followingEmailid,int(page_header), int(per_page_header))
                                    return success_response({'data': get_friends_post ,'Total-Post':total_Post,'Pagination': str(total_pages)})
                                return failure_response(statuscode='409', content=f'Not following')

                            return failure_response(statuscode='409', content=f'Not following')
                        get_friends_post, total_pages, total_Post = Get_Particular_friends_post(followingEmailid,
                                                                                                int(page_header),int(per_page_header))

                        return success_response({'data': get_friends_post, 'Total-Post': total_Post, 'Pagination': str(total_pages)})
                    return failure_response(statuscode='409', content=f'EmailId:{followingEmailid} does not exists/INACTIVE')
                return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def block_Friend():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                data = request.get_json()
                required_fields = ['followingEmailid']
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                followingEmailid = data['followingEmailid']
                if check_email_For_Username(emailid):
                    if check_email_For_Username(followingEmailid):
                        if not check_account_Type(followingEmailid): # IF NOT PUBLIC
                            if status_for_request(emailid, followingEmailid):
                                status = status_for_request(emailid, followingEmailid).status
                                print(status)
                                if status == 'ACCEPTED':
                                    block_friend(emailid,followingEmailid)
                                    return success_response('Blocked Successfully')
                                return failure_response(statuscode='409', content=f'Not following')
                            return failure_response(statuscode='409', content=f'Not following')
                        block_friend(emailid,followingEmailid)
                        return success_response('Blocked Successfully')

                    return failure_response(statuscode='409', content=f'EmailId:{followingEmailid} does not exists/INACTIVE')
                return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def unblock_Friend():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                data = request.get_json()
                required_fields = ['followingEmailid']
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                followingEmailid = data['followingEmailid']
                if check_email_For_Username(emailid):
                    if check_email_For_Username(followingEmailid):
                        if status_for_request(emailid, followingEmailid):
                            status = status_for_request(emailid, followingEmailid).status
                            print(status)
                            if status == 'BLOCK':
                                unblock_friend(emailid,followingEmailid)
                                return success_response('UnBlocked Successfully')
                            return failure_response(statuscode='409', content=f'Not Blocked')
                        return failure_response(statuscode='409', content=f'Not Blocked')
                    return failure_response(statuscode='409', content=f'EmailId:{followingEmailid} does not exists/INACTIVE')
                return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def block_list():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                page_header = request.headers.get('Page')
                per_page_header = request.headers.get('PerPage')
                if not page_header:
                    return failure_response(statuscode='401', content='page_header is missing')
                if not per_page_header:
                    return failure_response(statuscode='401', content='per_page_header is missing')
                if check_email_For_Username(emailid):
                    Get_block_List, total_pages,total_block_list= Get_block_list(emailid,int(page_header), int(per_page_header))
                    return success_response({'data': Get_block_List ,'Pagination': str(total_pages),'Total-Block':total_block_list})

                return failure_response(statuscode='409', content=f'EmailId:{emailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')



def like_The_Post():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                data= request.get_json()
                postid = data['postid']
                if check_postid(postid):
                    likepost(postid,emailid)
                    return success_response("Post Liked Successfully")
                return failure_response(statuscode='409', content=f'Postid : {postid} does not found')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def unlike_The_Post():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                data=request.get_json()
                postid=data['postid']
                if check_postid(postid):
                    if unlikepost(postid,emailid):
                        unlikepost(postid,emailid)
                        return success_response("Post UnLiked Successfully")
                    else:
                        return success_response("Post UnLiked already")
                return failure_response(statuscode='409', content=f'Postid :{postid} not found')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def filter_By_username():
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('PerPage')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
        data = request.get_json()
        required_fields = ['username']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        username = data['username']
        if check_username_existence(username):
            profile_info, total_following, total_followers, total_posts, total_pages = Get_Profile_Info_ByUsername(
                username, int(page_header), int(per_page_header))

            return success_response(
                {'data': profile_info, 'total_following': total_following, 'total_followers': total_followers,
                 'total_posts': total_posts, 'Pagination': total_pages})
        return failure_response(statuscode='409', content=f'EmailId:{username} does not exists/INACTIVE')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def search_Username():
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('PerPage')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
        data = request.get_json()
        required_fields = ['username']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        username = data['username']
        if username:
            # username,  total_pages = search_username(username, int(page_header), int(per_page_header))
            profile_info, total_following, total_followers, total_posts, total_pages,username = search_username(
                username, int(page_header), int(per_page_header))

            return success_response({'data': profile_info,'Pagination': total_pages,'total_following':total_following,'total_followers':total_followers,'total_posts':total_posts,'username':username})

        return failure_response(statuscode='409', content=f'EmailId:{username} does not exists/INACTIVE')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def post_Comments():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                data = request.get_json()
                required_fields = ['postid','comments']
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                postid = data['postid']
                comments = data['comments']
                if save_comments(postid,comments,emailid):
                    return success_response('Comments added Successfully')
                else:
                    return failure_response(statuscode='500', content=f'Comments Save Error')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def Reply_For_Comments():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                data = request.get_json()
                required_fields = ['commentid','replycomments']
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                commentid = data['commentid']
                replycomments = data['replycomments']
                if save_replycomments(commentid,replycomments,emailid):
                    return success_response('Reply Comments added Successfully')
                else:
                    return failure_response(statuscode='500', content=f'Reply Comments Save Error')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def delete_Comments():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                emailid = payload.get('EmailId')
                data = request.get_json()
                required_fields = ['commentid']
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                commentid = data['commentid']
                if deletecomment(emailid,commentid):
                    return success_response('Comments deleted Successfully')

                return failure_response(statuscode='409', content='Unable to delete (INCORRECT ACCESS/COMMENTID)')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def post_Messages():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                senderEmailid=payload.get('EmailId')
                required_fields = ['receiverEmailid','content']
                data = request.get_json()
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                receiverEmailid = data['receiverEmailid']
                content = data['content']
                read = False
                if check_email_For_Username(receiverEmailid):
                    if check_account_Type(receiverEmailid): # NOT PUBLIC
                        if status_for_request(senderEmailid,receiverEmailid):
                            status = status_for_request(senderEmailid, receiverEmailid).status
                            print(status)
                            if status == 'ACCEPTED':
                                if postMessages(senderEmailid,receiverEmailid,content,read):
                                    return success_response('Messages Posted Successfully')
                                return failure_response(statuscode='409', content=f'Message Post ERROR')
                            return failure_response(statuscode='409', content=f'NOT FOLLOWING')
                        return failure_response(statuscode='409', content=f'NOT FOLLOWING')

                    if postMessages(senderEmailid, receiverEmailid, content, read):
                        return success_response('Messages Posted Successfully')
                    return failure_response(statuscode='409', content=f'Message Post ERROR')

                return failure_response(statuscode='409', content=f'EmailId:{receiverEmailid} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def delete_Message():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                senderEmailid=payload.get('EmailId')
                required_fields = ['messageId']
                data = request.get_json()
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                messageId = data['messageId']
                print(messageId)
                if check_delete_access(senderEmailid,messageId):
                    if deleteMessage(senderEmailid,messageId):
                        return success_response('Messages Deleted Successfully')
                    return failure_response(statuscode='500', content=f'ERROR in deleting Messages')
                return failure_response(statuscode='500', content=f'Does not have right access to DELETE/DELETED ALREADY')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def get_Messages_BY_Emailid():
    try:
        token = request.headers.get('Authorization')
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('PerPage')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                Emailid=payload.get('EmailId')
                required_fields = ['friendId']
                data = request.get_json()
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                friendId = data['friendId']
                if check_email_For_Username(friendId):
                    if status_for_request(Emailid, friendId):
                        status = status_for_request(Emailid, friendId).status
                        print(status)
                        if status == 'ACCEPTED':
                            get_messages,total_pages=Get_entire_messages(Emailid,friendId,page_header,per_page_header)
                            return success_response({'data': get_messages,'Pagination':total_pages})
                        return failure_response(statuscode='409', content=f'NOT FOLLOWING')
                    return failure_response(statuscode='409', content=f'NOT FOLLOWING')
                return failure_response(statuscode='409', content=f'EmailId:{friendId} does not exists/INACTIVE')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def update_Read_Status():  # ( SINGLE MESSAGES UPDATED / NOT ALL THE MESSAGES AT A TIME )
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                Emailid = payload.get('EmailId')
                required_fields = ['messageId']
                data = request.get_json()
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                messageId = data['messageId']
                if check_delete_access(Emailid, messageId):
                    if update_Message_Status(messageId):
                        return success_response('Message READ STATUS: TRUE')
                    return failure_response(statuscode='500', content=f'Update ERROR')
                return failure_response(statuscode='500', content=f'Does not have right access to UPDATE/DELETED ALREADY')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def get_Post_By_Hashtags():
    try:
        token = request.headers.get('Authorization')
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('PerPage')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                Emailid = payload.get('EmailId')
                required_fields = ['hashtag']
                data = request.get_json()
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                hashtag = data['hashtag']
                if check_for_hashtags(hashtag):
                    data = []
                    postid=check_for_hashtags(hashtag)
                    for id in postid:
                        post_info,total_pages=get_posts(id,page_header,per_page_header)

                        data.append( {'Post_info': post_info,'Total_pages':total_pages})
                    return success_response({'data':data})
                return failure_response(statuscode='400', content='Hashtag Not Available')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def change_Password():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                Emailid = payload.get('EmailId')
                required_fields = ['oldpassword','newpassword']
                data = request.get_json()
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                oldpassword = data['oldpassword']
                newpassword = data['newpassword']
                user = check_login(Emailid, oldpassword)
                if user:
                    if update_password(Emailid,newpassword):
                        return success_response('Password changed successfully')
                    return failure_response(statuscode='400', content='unable to change the IOldPassword')
                return failure_response(statuscode='400', content='OldPassword Incorrect')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def forgotPassword():
    try:
        from app.utils.emailSender import otpSending
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                EmailId = payload.get('EmailId')
                if check_email_For_Username(EmailId):
                    try:
                        global_otp, global_Email = otpSending(EmailId)
                        print(global_Email, global_otp)
                        session['global_OTP'] = global_otp
                        session['global_EMAILID'] = global_Email
                        return success_response('OTP sent Successfully')
                    except Exception as e:
                        print(f"Error: {e}")
                        return failure_response(statuscode='500', content='ERROR: Occurred in OTP sending')

                return failure_response(statuscode='409', content=f'EmailId: {EmailId} does not exists')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content='An unexpected error occurred.')

        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def verify_OTP():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                EmailId = payload.get('EmailId')
                required_fields = ['OTP']
                data = request.get_json()
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                OTP = data['OTP']
                if check_email_For_Username(EmailId):
                    try:
                        stored_otp = session.get('global_OTP')
                        stored_email = session.get('global_EMAILID')
                        if EmailId == stored_email and OTP == stored_otp:
                            return success_response('OTP Valid')
                        else:
                            return failure_response(statuscode='500', content='Invalid OTP')
                    except Exception as e:
                        print(f"Error: {e}")
                        return failure_response(statuscode='500', content='An unexpected error occurred.')
                return failure_response(statuscode='409', content=f'EmailId: {EmailId} does not exists')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content='An unexpected error occurred.')

        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')

def change_Password_By_Otp():
    try:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=10)
                EmailId = payload.get('EmailId')
                required_fields = ['newpassword']
                data = request.get_json()
                for field in required_fields:
                    if field not in data or not data[field]:
                        return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
                newpassword = data['newpassword']
                if check_email_For_Username(EmailId):
                    if update_password(EmailId,newpassword):
                        return success_response('New password Changed Successfully')
                    return failure_response(statuscode='409',content='Unable to change Password')
                return failure_response(statuscode='409', content=f'EmailId: {EmailId} does not exists')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500', content='An unexpected error occurred.')

        return failure_response(statuscode='409', content='Token is missing')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')
