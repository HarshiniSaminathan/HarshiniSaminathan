
from flask import jsonify, request
from app.controller.user_controllor import fetch_user_data, get_total_records, insert_user, check_email_existence, update_user, get_user_by_email, delete_user
from app.response import success,failure
from app.strings import success_res,failure_res
from app.utils.validator_utils import is_email_id,is_valid_password
def get_users():
    page = request.args.get('page', default=1, type=int)
    items_per_page = 10
    offset = (page - 1) * items_per_page

    data = fetch_user_data(items_per_page, offset)
    total_records = get_total_records()
    return success(data, {'X-Total-Count': str(total_records)})

def add_user():
    data = request.get_json()
    emailid = data.get('emailid')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    mobileno = data.get('mobileno')
    dob = data.get('dob')
    address = data.get('address')
    try:
        if check_email_existence(emailid):
            return failure("Email already exists", '409')

        insert_user(emailid, firstname, lastname, mobileno, dob, address)
        return success(success_res,'user added sucessfully')
    except Exception as e:
        print(f"Error: {e}")
        return failure(message=str(e),status_code='400')

def check_email(emailid):
    if check_email_existence(emailid):
        return failure(failure_res,'400')
    else:
        return success(success_res, 'Email does not exists')
def edit_user(emailid):
    if request.method == 'PUT':
        try:
            data = request.get_json()
            emailid = data['emailid']
            firstname = data['firstname']
            lastname = data['lastname']
            mobileno = data['mobileno']
            dob = data['dob']
            address = data['address']
            update_user(emailid, firstname, lastname, mobileno, dob, address)
            return success(success_res, 'user updated successfully')
        except Exception as e:
            print(f"Error: {e}")
            return failure(str(e), '500')
    if request.method == 'GET':
        res = get_user_by_email(emailid)
        return success(success_res, res)

def delete_user_route(emailid):
    try:
        if not check_email_existence(emailid):
            return failure("Email does not exists", '409')
        delete_user(emailid)
        return success(success_res, 'user deleted')
    except Exception as e:
        print(f"Error: {e}")
        return failure(message=str(e), status_code='400')

def validate_user_email(emailid):
    try:
        if is_email_id(email_id=emailid):
            return success(success_res, 'Emailid valid')
        else:
            return failure(message='Emailid not valid',status_code='400')
    except Exception as e:
        print(f"Error: {e}")
        return failure(message=str(e), status_code='400')

def validate_user_password():
    try:
        data = request.get_json()
        password = data['password']
        if is_valid_password(password):
            return success(success_res, 'Strong password')
        else:
            return failure(message='Weak password', status_code='400')
    except Exception as e:
        print(f"Error: {e}")
        return failure(message=str(e), status_code='400')



