from flask import request
import base64

from app.response import failure_response, success_response
from app.controller.userController import check_email_existence
from app.controller.adminController import insert_doctor,insert_role_password,updateSlots,fetch_doctor_records,get_total_doctor,insert_admin,fetch_admin_records,get_total_admin,insert_slot,check_slot_inserted

def register_doctor():
    try:
        data = request.get_json()
        required_fields = ['doctorName', 'doctorPhoneNumber', 'doctorAddress', 'doctorExperience',
                            'doctorSpecialization', 'doctorEmailId', 'doctorSpecializationProof', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')

        doctorName = data['doctorName']
        doctorPhoneNumber = data['doctorPhoneNumber']
        doctorAddress = data['doctorAddress']
        doctorExperience = data['doctorExperience']
        doctorSpecialization = data['doctorSpecialization']
        doctorEmailId = data['doctorEmailId']
        doctorSpecializationProof = data['doctorSpecializationProof']
        password = data['password']
        role = "DOCTOR"
        if check_email_existence(doctorEmailId):
            return failure_response(statuscode='409', content='Email id already exists')
        try:
            binary_data = base64.b64decode(doctorSpecializationProof)
        except Exception as e:
            return failure_response(statuscode='400', content='Invalid base64 encoding for doctorSpecializationProof')
        print(f"Encoded data: {doctorSpecializationProof}")
        print(f"Decoded data: {binary_data}")
        insert_role_password(doctorEmailId, password, role)
        insert_doctor(doctorName, doctorPhoneNumber, doctorAddress, doctorExperience,
                      doctorSpecialization, binary_data, doctorEmailId)
        return success_response('Doctor Added Successfully')

    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def get_Register_Doctor_Records():
    data= fetch_doctor_records()
    total_doctors= get_total_doctor()
    return success_response({'data': data, 'Doctor-Total-Count': str(total_doctors)})


def register_Admin():
    try:
        data = request.get_json()
        required_fields = ['adminName', 'adminPhoneNumber', 'adminAddress', 'emailId',
                            'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')

        adminName = data['adminName']
        adminPhoneNumber = data['adminPhoneNumber']
        adminAddress = data['adminAddress']
        emailId  = data['emailId']
        password= data['password']
        role = "ADMIN"
        if check_email_existence(emailId):
            return failure_response(statuscode='409', content='Email id already exists')
        insert_role_password(emailId, password, role)
        insert_admin(adminName, adminPhoneNumber, adminAddress, emailId)
        return success_response('Admin Added Successfully')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def get_Register_Admin_Records():
    data = fetch_admin_records()
    total_admin = get_total_admin()
    return success_response({'data': data, 'Admin-Total-Count': str(total_admin)})


def add_Slot_To_Doctors():
    try:
        data = request.get_json()
        required_fields = ['doctorEmailId','slotStartTime','slotEndTime']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        doctorEmailId = data['doctorEmailId']
        slotStartTime = data['slotStartTime']
        slotEndTime = data['slotEndTime']
        slotStatus = True    #  initially slotstatus will be True
        if check_email_existence(doctorEmailId):
            if check_slot_inserted(doctorEmailId,slotStartTime):
                return failure_response(statuscode='409', content='Ths slot timimgs inserted already')

            insert_slot(doctorEmailId, slotStartTime, slotStatus, slotEndTime)
            return success_response('Slot Added Successfully')

        return failure_response(statuscode='409', content='Email id does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def update_Slots_status(doctorEmailId):
    if check_email_existence(doctorEmailId):
        try:
            data = request.get_json()
            slotStatus = data['slotStatus']
            slotStartTime = data['slotStartTime']
            slotEndTime = data['slotEndTime']
            if check_email_existence(doctorEmailId):
                updateSlots(doctorEmailId,slotStartTime, slotEndTime,slotStatus)
                return success_response('Slots updated successfully')
            return failure_response(statuscode='409', content='Email id does not exists')
        except Exception as e:
            print(f"Error: {e}")
            return failure_response(statuscode='500', content=str(e))
    else:
        return failure_response(statuscode='500',content='Emailid Does Not Exists')