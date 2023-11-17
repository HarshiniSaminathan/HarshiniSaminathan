
from flask import request
from app.controller.user_controllor import fetch_user_data, get_total_records, insert_user, check_email_existence, update_user, get_user_by_email, delete_user,common_email_present,data_from_common_email
from app.response import success_response,failure_response
from app.utils.validator_utils import is_email_id,is_valid_password

def get_users():
    page = request.args.get('page', default=1, type=int)
    items_per_page = 10
    offset = (page - 1) * items_per_page
    data = fetch_user_data(items_per_page, offset)
    total_records = get_total_records()
    return success_response({'data':data,'X-Total-Count': str(total_records)})

def add_user():
    try:
        data = request.get_json()
        emailid = data.get('emailid')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        mobileno = data.get('mobileno')
        dob = data.get('dob')
        address = data.get('address')
        if check_email_existence(emailid):
            return failure_response(statuscode='409',content='Emailid already exists')
        insert_user(emailid, firstname, lastname, mobileno, dob, address)
        return success_response('User Added Sucessfully')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='400',content=str(e))

def check_email(emailid):
    if check_email_existence(emailid):
        return success_response('Emailid Already exists')
    else:
        return failure_response(statuscode='409',content='Emailid Does Not Exists')

def edit_user(emailid):
    if check_email_existence(emailid):
        if request.method == 'PUT':
            try:
                data = request.get_json()
                firstname = data['firstname']
                lastname = data['lastname']
                mobileno = data['mobileno']
                dob = data['dob']
                address = data['address']
                update_user(emailid,firstname, lastname, mobileno, dob, address)
                return success_response('user updated successfully')
            except Exception as e:
                print(f"Error: {e}")
                return failure_response(statuscode='500',content=str(e))
        if request.method == 'GET':
                res = get_user_by_email(emailid)
                return success_response({'data':res})
    else:
        return failure_response(statuscode='500',content='Emailid Does Not Exists')

def delete_user_route(emailid):
    try:
        if not check_email_existence(emailid):
            return failure_response(statuscode='500',content='Emailid Does Not Exists')
        delete_user(emailid)
        return success_response('User Deleted Successfully')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='400', content=str(e))

def validate_user_email(emailid):
    try:
        if is_email_id(email_id=emailid):
            return success_response('Emailid Valid')
        else:
            return failure_response(statuscode='400',content='Emailid Invalid')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='400',content=str(e))

def validate_user_password():
    try:
        data = request.get_json()
        password = data['password']
        if is_valid_password(password):
            return success_response('Strong Password')
        else:
            return failure_response(statuscode='400',content='Weak password')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='400',content=str(e))


def get_user_or_vendor_by_email(emailid):
    if common_email_present(emailid):
        datas=data_from_common_email(emailid)
        return success_response({'data': datas})
    else:
        return failure_response(statuscode='500',content='Emailid Does Not Exists')



