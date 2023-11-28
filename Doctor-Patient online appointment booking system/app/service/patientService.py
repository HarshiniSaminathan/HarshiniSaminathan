import json
import os

from flask import request, jsonify
import base64
from app.models.medicalRecordsModel import PMRecordTable
from werkzeug.utils import secure_filename

from app.controller.adminController import insert_role_password
from app.controller.userController import check_email_existence
from app.response import failure_response, success_response
from app.controller.patientController import (insert_patient, get_Prescription, add_Feedback_To_Admin,
                                              add_Feedback_To_Doctor, addPMReport, findAppointmnetId,
                                              check_appointmentAccepted, patient_appointments,
                                              countOfAppointmentsPerDay, doctorForSpecialization_exists,
                                              doctor_for_Specialization, check_for_slotsPending,
                                              fetch_Availabledoctor_records, prescription_datas,
                                              check_for_slotsRejected, updateProfile, check_for_slotsNotRequested,
                                              fetch_slotsfor_doctor, requestingAppointmnet, appointmentNotBooked,
                                              alreadyRequestedForSameDateTime, add_filePMReport)



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
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('Per-Page')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
        data,total_page= fetch_Availabledoctor_records(int(page_header),int(per_page_header))
        return success_response({'data': data,'Pagination':total_page})
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def profile_upadte(patientEmailId):
    try:
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
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def get_slotsfor_doctor(doctorEmailId):
    try:
        if check_email_existence(doctorEmailId):
            data= fetch_slotsfor_doctor(doctorEmailId)
            return success_response({'data': data})
        return failure_response(statuscode='409', content='Email id does exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def requesting_for_appointment(patientEmailId):
    from app.utils.emailSender import send_appointment_confirmation_email
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
                        send_appointment_confirmation_email(doctor_email=doctorEmailId, patient_email=patientEmailId, appointment_date=appointmentDate,
                                                            appointment_time=appointmentTime)
                        return success_response('Appointment Requested and Email sent')
                    return failure_response(statuscode='409', content=f'Already your appointment for DATE:{appointmentDate} and TIME:{appointmentTime} was REJECTED')
                return failure_response(statuscode='409', content='Appointment for this Date and Time already Booked')
            return failure_response(statuscode='409', content='Email id does not exists')
        return failure_response(statuscode='409', content='Email id does not exists')

    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def get_patient_appointments(patientEmailId):
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('Per-Page')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
        if check_email_existence(patientEmailId):
            total_appointments,total_records=patient_appointments(patientEmailId,int(page_header),int(per_page_header))
            return success_response({"data":total_appointments,'Pagination':total_records})
        return failure_response(statuscode='409', content=f'Email id :{patientEmailId} does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')

def count_appointments(patientEmailId):
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('Per-Page')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
        count_appointments_result,total_page = countOfAppointmentsPerDay(patientEmailId,int(page_header),int(per_page_header))

        result = [
            {
                "date": appointment['date'],
                "appointmentCount": appointment['appointmentCount']
            }
            for appointment in count_appointments_result
        ]

        return success_response({"Appointments-Count-With-DATE": result,'Pagination':total_page})
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def get_By_DoctorSpecialization():
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('Per-Page')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
        try:
            data=request.get_json()
            required_fields = ['doctorSpecialization']
            for field in required_fields:
                if field not in data or not data[field]:
                    return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
            doctorSpecialization = data['doctorSpecialization']
            doctorSpecialization1=doctorSpecialization.upper()
            if doctorForSpecialization_exists(doctorSpecialization):
                result,total_page=doctor_for_Specialization(doctorSpecialization,int(page_header),int(per_page_header))
                return success_response({f'data: {doctorSpecialization1}': result,'Pagination':total_page})
            return failure_response(statuscode='409', content=f'Doctor not available for {doctorSpecialization1}')
        except Exception as e:
            print(f"Error: {e}")
            return failure_response(statuscode='500', content='An unexpected error occurred.')
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
                        from app.utils.emailSender import send_PMR_Report
                        send_PMR_Report(doctor_email=doctorEmailId, patient_email=patientEmailId, appointment_time=appointmentTime, PMReport=PMReport, appointment_date=appointmentDate,
                                        description=description)
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

def upload_PMReport():
    try:
        from app.utils.commanUtils import add_in_entity
        from run import UPLOAD_FOLDER
        file = request.files['file']
        # data = request.form.to_dict()
        form_data = request.form.get('data')
        try:
            data = json.loads(form_data)
        except json.JSONDecodeError:
            return failure_response(statuscode='400', content='Invalid JSON data')
        doctorEmailId = data['doctorEmailId']
        patientEmailId = data['patientEmailId']
        appointmentDate = data['appointmentDate']
        appointmentTime = data['appointmentTime']
        description = data['description']
        if check_email_existence(doctorEmailId):
            if check_email_existence(patientEmailId):
                if check_appointmentAccepted(doctorEmailId,patientEmailId,appointmentDate,appointmentTime):
                    try:
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(UPLOAD_FOLDER, filename))
                        appointmentId = findAppointmnetId(doctorEmailId, patientEmailId, appointmentDate,
                                                          appointmentTime)
                        add_filePMReport(appointmentId,filename,description)
                        return success_response("PMReports Added successfully")
                    except Exception as e:
                        print(f"Error saving PMReport file: {e}")
                        return failure_response(statuscode='400', content='Error saving PMReport file')
                return failure_response(statuscode='409', content="Appointment not ACCEPTED")
            return failure_response(statuscode='409', content=f'EmailId:{patientEmailId} does not exists')
        return failure_response(statuscode='409', content=f'EmailId:{doctorEmailId} does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')

def view_prescription():
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('Per-Page')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
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
                    prescriptiondatas,total_pages = prescription_datas(appointmentId,int(page_header),int(per_page_header))
                    return success_response({"datas":prescriptiondatas,'Pagination':total_pages})
                return failure_response(statuscode='409', content=f'No appointments on DATE:{appointmentDate} TIME:{appointmentTime}')
            return failure_response(statuscode='409', content=f'EmailId:{patientEmailId} does not exists')
        return failure_response(statuscode='409', content=f'EmailId:{doctorEmailId} does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def add_Feedback():
    try:
        data = request.get_json()
        required_fields = ['patientEmailId', 'feedbackText', 'rating']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        patientEmailId = data['patientEmailId']
        feedbackText = data['feedbackText']
        rating = data['rating']
        doctorEmailId = data['doctorEmailId']
        if not check_email_existence(patientEmailId):
            return failure_response(statuscode='409', content=f'EmailId: {patientEmailId} does not exist')
        if doctorEmailId and not check_email_existence(doctorEmailId):
            return failure_response(statuscode='409', content=f'EmailId: {doctorEmailId} does not exist')

        if doctorEmailId != None:
            add_Feedback_To_Doctor(patientEmailId, doctorEmailId, feedbackText, rating)
        else:
            add_Feedback_To_Admin(patientEmailId, feedbackText, rating)
        return success_response("Feedback added successfully")

    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')

def get_All_Prescription():
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('Per-Page')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
        data = request.get_json()
        required_fields = ['patientEmailId', 'doctorEmailId']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        patientEmailId = data['patientEmailId']
        doctorEmailId = data['doctorEmailId']
        if check_email_existence(patientEmailId):
            if check_email_existence(doctorEmailId):
                reports,total_page = get_Prescription(patientEmailId, doctorEmailId,int(page_header),int(per_page_header))
                return success_response({"data": reports,"Pagination":total_page})
            return failure_response(statuscode='409', content=f'EmailId:{doctorEmailId} does not exists')
        return failure_response(statuscode='409', content=f'EmailId:{patientEmailId} does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


