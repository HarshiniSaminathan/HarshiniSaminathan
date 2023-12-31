import json

from flask import request
from werkzeug.utils import secure_filename

from app.controller.adminController import fetch_inactiveUser_records, activate_user, fetch_active_user_records,fetch_inactive_post
from app.controller.userController import check_username_existence, check_email_existence, check_email_For_Username,activatePost
from app.response import failure_response, success_response


def get_All_InactiveUser():
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('PerPage')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')

        inactive_users, total_pages = fetch_inactiveUser_records(int(page_header), int(per_page_header))

        return success_response({'data': inactive_users,'Pagination': str(total_pages)})
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def activating_The_Users():
    try:
        data = request.get_json()
        required_fields = ['emailid']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        emailid = data['emailid']
        status = "ACTIVE"
        if  check_email_existence(emailid):
            if not check_email_For_Username(emailid):
                activate_user(emailid, status)
                return success_response('User Activated Successfully')
            return failure_response(statuscode='409', content='Emailid alreday get activated')
        return failure_response(statuscode='409', content='Emailid does not exits')

    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def get_All_ActivatedUsers():
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('PerPage')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')

        active_users, total_pages = fetch_active_user_records(int(page_header), int(per_page_header))

        return success_response({'data': active_users,'Pagination': str(total_pages)})
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def activating_The_Post():
    try:
        data = request.get_json()
        postid=data['postid']
        status = 'ACTIVE'
        if postid:
            if activatePost(postid,status):
                return success_response("Post Activated Successfully")
            else:
                return failure_response(statuscode='409', content=f'Already POST Activated')
        return failure_response(statuscode='409', content=f'postid:{postid} does not exists/INACTIVE')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred ,{e}.')


def get_Inactive_Posts():
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('PerPage')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')

        inactive_post, total_pages = fetch_inactive_post(int(page_header), int(per_page_header))

        return success_response({'data': inactive_post ,'Pagination': str(total_pages)})
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')