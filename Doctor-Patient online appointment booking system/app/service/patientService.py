from flask import request
import base64
from app.controller.adminController import insert_role_password
from app.controller.userController import check_email_existence
from app.response import failure_response, success_response
from app.controller.patientController import (insert_patient,addPMReport,findAppointmnetId,check_appointmentAccepted,patient_appointments,countOfAppointmentsPerDay,doctorForSpecialization_exists,doctor_for_Specialization,check_for_slotsPending,
            fetch_Availabledoctor_records,prescription_datas,check_for_slotsRejected,updateProfile,check_for_slotsNotRequested,fetch_slotsfor_doctor,requestingAppointmnet,appointmentNotBooked,alreadyRequestedForSameDateTime)


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


def get_patient_appointments(patientEmailId):
    total_appointments=patient_appointments(patientEmailId)
    return success_response({"data":total_appointments})


def count_appointments(patientEmailId):
    count_appointments_result = countOfAppointmentsPerDay(patientEmailId)

    result = [
        {
            "date": appointment['date'],
            "appointmentCount": appointment['appointmentCount']
        }
        for appointment in count_appointments_result
    ]

    return success_response({"Appointments-Count-With-DATE": result})


def get_By_DoctorSpecialization():
    try:
        data=request.get_json()
        required_fields = ['doctorSpecialization']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        doctorSpecialization = data['doctorSpecialization']
        doctorSpecialization1=doctorSpecialization.upper()
        if doctorForSpecialization_exists(doctorSpecialization):
            result=doctor_for_Specialization(doctorSpecialization)
            return success_response({f'data: {doctorSpecialization1}': result})
        return failure_response(statuscode='409', content=f'Doctor not available for {doctorSpecialization1}')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def Check_Slot_Availability_Doctor():
    try:
        data=request.get_json()
        required_fields = ['doctorEmailId','appointmentDate']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        doctorEmailId=data['doctorEmailId']
        appointmentDate=data['appointmentDate']
        if check_email_existence(doctorEmailId):
            SlotsInPending=check_for_slotsPending(doctorEmailId,appointmentDate)
            SlotsInRejected=check_for_slotsRejected(doctorEmailId,appointmentDate)
            SlotsNotRequested=check_for_slotsNotRequested(doctorEmailId,appointmentDate)
            return success_response({'PENDING SLOTS':SlotsInPending,'REJECTED SLOTS':SlotsInRejected,'SLOTS NOT REQUESTED':SlotsNotRequested})
        return failure_response(statuscode='409', content='Email id does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def add_PMReports():
    try:
        data=request.get_json()
        doctorEmailId=data['doctorEmailId']
        patientEmailId=data['patientEmailId']
        appointmentDate=data['appointmentDate']
        appointmentTime=data['appointmentTime']
        PMReport=data['PMReport']
        description=data['description']
        if check_email_existence(doctorEmailId):
            if check_email_existence(patientEmailId):
                if check_appointmentAccepted(doctorEmailId,patientEmailId,appointmentDate,appointmentTime):
                    try:
                        binary_data = base64.b64decode(PMReport)
                        print(binary_data)
                        appointmentId = findAppointmnetId(doctorEmailId, patientEmailId, appointmentDate,
                                                          appointmentTime)
                        addPMReport(appointmentId, binary_data, description)
                        return success_response("PMReports Added successfully")
                    except Exception as e:
                        return failure_response(statuscode='400',
                                                content='Invalid base64 encoding for doctorSpecializationProof')
                return failure_response(statuscode='409', content="Appointment not ACCEPTED")
            return failure_response(statuscode='409', content=f'EmailId:{patientEmailId} does not exists')
        return failure_response(statuscode='409', content=f'EmailId:{doctorEmailId} does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def view_prescription():
    data = request.get_json()
    doctorEmailId = data['doctorEmailId']
    patientEmailId = data['patientEmailId']
    appointmentDate = data['appointmentDate']
    appointmentTime = data['appointmentTime']
    if check_email_existence(doctorEmailId):
        if check_email_existence(patientEmailId):
            if check_appointmentAccepted(doctorEmailId, patientEmailId, appointmentDate, appointmentTime):
                appointmentId = findAppointmnetId(doctorEmailId, patientEmailId, appointmentDate,
                                                  appointmentTime)
                prescriptiondatas = prescription_datas(appointmentId)
                return success_response({"datas":prescriptiondatas})
            return failure_response(statuscode='409', content=f'No appointments on DATE:{appointmentDate} TIME:{appointmentTime}')
        return failure_response(statuscode='409', content=f'EmailId:{patientEmailId} does not exists')
    return failure_response(statuscode='409', content=f'EmailId:{doctorEmailId} does not exists')
