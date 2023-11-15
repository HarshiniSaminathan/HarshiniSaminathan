
from flask import jsonify, request
from app.controller.user_controllor import fetch_user_data, get_total_records, insert_user, check_email_existence, update_user, get_user_by_email, delete_user

def get_users():
    page = request.args.get('page', default=1, type=int)
    items_per_page = 10
    offset = (page - 1) * items_per_page

    data = fetch_user_data(items_per_page, offset)
    total_records = get_total_records()

    return jsonify(data), 200, {'X-Total-Count': str(total_records)}

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
            return jsonify(success=False, error='Email already exists'), 400

        insert_user(emailid, firstname, lastname, mobileno, dob, address)
        return jsonify(success=True)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify(success=False, error=str(e)), 500

def check_email(emailid):
    if check_email_existence(emailid):
        return jsonify(success=True)
    else:
        return jsonify(success=False)

def edit_user(emailid):
    if request.method == 'PUT':
        data = request.get_json()
        emailid = data['emailid']
        firstname = data['firstname']
        lastname = data['lastname']
        mobileno = data['mobileno']
        dob = data['dob']
        address = data['address']
        try:
            update_user(emailid, firstname, lastname, mobileno, dob, address)
            return jsonify(success=True)
        except Exception as e:
            print(f"Error: {e}")
            return jsonify(success=False, error=str(e)), 500
    else:
        res = get_user_by_email(emailid)
        return jsonify(res)

def delete_user_route(emailid):
    delete_user(emailid)
    return jsonify(success=True)
