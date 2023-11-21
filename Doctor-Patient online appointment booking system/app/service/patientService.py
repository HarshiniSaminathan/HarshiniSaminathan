from flask import request

from app.controller.adminController import insert_role_password
from app.controller.userController import check_email_existence
from app.response import failure_response, success_response
from app.controller.patientController import insert_patient,fetch_Availabledoctor_records,updateProfile,fetch_slotsfor_doctor,requestingAppointmnet,appointmentNotBooked,alreadyRequestedForSameDateTime


def register_New_Patient():
    try:
        data = request.get_json()
        required_fields = ['patientFirstName', 'patientLastName', 'patientPhoneNumber','patientDOB','patientAddress','patientEmailId',
                            'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')

        patientFirstName = data['patientFirstName']
        patientLastName = data['patientLastName']
        patientPhoneNumber = data['patientPhoneNumber']
        patientDOB=data['patientDOB']
        patientAddress=data['patientAddress']
        patientEmailId= data['patientEmailId']
        password= data['password']
        role = "PATIENT"
        if check_email_existence(patientEmailId):
            return failure_response(statuscode='409', content='Email id already exists')
        insert_role_password(patientEmailId, password, role)
        insert_patient(patientFirstName,patientLastName, patientPhoneNumber,patientDOB,patientAddress,patientEmailId)
        return success_response('Patient Added Successfully')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def get_Available_Doctors():
    data= fetch_Availabledoctor_records()
    return success_response({'data': data})


def profile_upadte(patientEmailId):
    if check_email_existence(patientEmailId):
        try:
            data=request.get_json()
            patientFirstName = data['patientFirstName']
            patientLastName = data['patientLastName']
            patientPhoneNumber = data['patientPhoneNumber']
            patientDOB=data['patientDOB']
            patientAddress=data['patientAddress']
            updateProfile(patientFirstName,patientLastName, patientPhoneNumber,patientDOB,patientAddress,patientEmailId)
            return success_response('patient updated successfully')
        except Exception as e:
            print(f"Error: {e}")
            return failure_response(statuscode='500', content=str(e))
    else:
        return failure_response(statuscode='500',content='Emailid Does Not Exists')


def get_slotsfor_doctor(doctorEmailId):
    if check_email_existence(doctorEmailId):
        data = fetch_slotsfor_doctor(doctorEmailId)
        return success_response({'data': data})
    return failure_response(statuscode='409', content='Email id does exists')


def requesting_for_appointment(patientEmailId):
    try:
        data = request.get_json()
        required_fields = ['doctorEmailId', 'appointmentDate', 'appointmentTime']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        doctorEmailId= data['doctorEmailId']
        appointmentDate = data['appointmentDate']
        appointmentTime = data['appointmentTime']
        appointmentStatus="PENDING"
        if check_email_existence(patientEmailId):
            if check_email_existence(doctorEmailId):
                if appointmentNotBooked(doctorEmailId,appointmentDate,appointmentTime):
                    if alreadyRequestedForSameDateTime(doctorEmailId,appointmentDate,appointmentTime,patientEmailId):
                        requestingAppointmnet(doctorEmailId,appointmentDate, appointmentTime,appointmentStatus,patientEmailId)
                        return success_response('Appointment Requested')
                    return failure_response(statuscode='409', content=f'Already your appointment for DATE:{appointmentDate} and TIME:{appointmentTime} was REJECTED')
                return failure_response(statuscode='409', content='Appointment for this Date and Time already Booked')
            return failure_response(statuscode='409', content='Email id does not exists')
        return failure_response(statuscode='409', content='Email id does not exists')

    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')

