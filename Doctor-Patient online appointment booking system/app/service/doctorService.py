import base64
import json
import os

from flask import request,send_file

from app.controller.adminController import findDoctorId
from app.controller.patientController import check_appointmentAccepted, findAppointmnetId, findPatientId
from app.controller.userController import check_email_existence
from app.response import failure_response, success_response
from app.controller.doctorController import (respondingAppointments,doctor_appointments,get_patient_PMReports,findPMRecord,
                                             countOfAppointmentsPerDay,addPrescription,addFeedbackResponse,get_feedbacks)



def responding_for_appointment(doctorEmailId):
    from app.utils.emailSender import send_appointment_Status
    try:
        data = request.get_json()
        required_fields = ['patientEmailId', 'appointmentDate', 'appointmentTime','appointmentStatus']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        patientEmailId = data['patientEmailId']
        appointmentDate = data['appointmentDate']
        appointmentTime = data['appointmentTime']
        appointmentStatus=data['appointmentStatus']
        if check_email_existence(patientEmailId):
            if check_email_existence(doctorEmailId):
                respondingAppointments(doctorEmailId,appointmentDate, appointmentTime,appointmentStatus,patientEmailId)
                send_appointment_Status(doctor_email=doctorEmailId, patient_email=patientEmailId,
                                                    appointment_date=appointmentDate,
                                                    appointment_time=appointmentTime,appointmentStatus=appointmentStatus)
                return success_response(f'Appointment Responded as : {appointmentStatus}')
            return failure_response(statuscode='409', content='Email id does not exists')
        return failure_response(statuscode='409', content='Email id does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def get_doctor_appointments(doctorEmailId):
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('Per-Page')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
        total_appointments,total_pages=doctor_appointments(doctorEmailId,int(page_header), int(per_page_header))
        return success_response({"data":total_appointments,"Pagination":total_pages})
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')

def count_appointments(doctorEmailId):
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('Per-Page')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
        count_appointments_result,total_page= countOfAppointmentsPerDay(doctorEmailId,int(page_header), int(per_page_header))
        result = [
            {
                "date": appointment['date'],
                "appointmentCount": appointment['appointmentCount']
            }
            for appointment in count_appointments_result
        ]
        return success_response({"Appointments-Count-With-DATE": result,"Pagination":total_page})
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')

def add_Prescription():
    try:
        data=request.get_json()
        doctorEmailId = data['doctorEmailId']
        patientEmailId = data['patientEmailId']
        appointmentDate = data['appointmentDate']
        appointmentTime = data['appointmentTime']
        medication=data['medication']
        dosage=data['dosage']
        instruction=data['instruction']
        try:
            if check_email_existence(doctorEmailId):
                if check_email_existence(patientEmailId):
                    if check_appointmentAccepted(doctorEmailId,patientEmailId,appointmentDate,appointmentTime):
                            appointmentId = findAppointmnetId(doctorEmailId, patientEmailId, appointmentDate,
                                                              appointmentTime)
                            addPrescription(appointmentId, medication, dosage,instruction)
                            return success_response("Prescription Added successfully")
                    return failure_response(statuscode='409', content="Appointment not ACCEPTED")
                return failure_response(statuscode='409', content=f'EmailId:{patientEmailId} does not exists')
            return failure_response(statuscode='409', content=f'EmailId:{doctorEmailId} does not exists')
        except Exception as e:
            print(f"Error: {e}")
            return failure_response(statuscode='500', content='An unexpected error occurred.')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def response_For_Feedback_():
    try:
        data = request.get_json()
        required_fields = ['patientEmailId', 'feedbackText', 'rating', 'feedbackResponse','doctorEmailId']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        patientEmailId = data['patientEmailId']
        feedbackText = data['feedbackText']
        rating = data['rating']
        doctorEmailId=data['doctorEmailId']
        feedbackResponse = data['feedbackResponse']
        try:
            patientId = findPatientId(patientEmailId)
            doctorId =findDoctorId(doctorEmailId)
            print(patientId, feedbackText, rating, feedbackResponse,doctorId)
            addFeedbackResponse(patientId, feedbackText, rating, feedbackResponse,doctorId)
            return success_response('FeedbackResponse added successfully')
        except Exception as e:
            print(f"Error: {e}")
            return failure_response(statuscode='500', content=str(e))
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')


def get_All_Feedbacks():
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('Per-Page')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
        data=request.get_json()
        required_fields = ['doctorEmailId']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        doctorEmailId = data['doctorEmailId']
        if check_email_existence(doctorEmailId):
            feedbacks,total_recors=get_feedbacks(doctorEmailId, int(page_header),int(per_page_header))
            return success_response({"data":feedbacks,"Pagination":total_recors})
        return failure_response(statuscode='409', content=f'EmailId:{doctorEmailId} does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')

def get_All_PMReports():
    try:
        page_header = request.headers.get('Page')
        per_page_header = request.headers.get('Per-Page')
        if not page_header:
            return failure_response(statuscode='401', content='page_header is missing')
        if not per_page_header:
            return failure_response(statuscode='401', content='per_page_header is missing')
        data = request.get_json()
        required_fields = ['patientEmailId','doctorEmailId']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')
        patientEmailId=data['patientEmailId']
        doctorEmailId=data['doctorEmailId']
        if check_email_existence(patientEmailId):
            if check_email_existence(doctorEmailId):
                reports,total_page=get_patient_PMReports(patientEmailId,doctorEmailId,int(page_header),int(per_page_header))
                return success_response({"data": reports,"Pagination":total_page})
            return failure_response(statuscode='409', content=f'EmailId:{doctorEmailId} does not exists')
        return failure_response(statuscode='409', content=f'EmailId:{patientEmailId} does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')

def download_PMReports():
    try:
        data = request.get_json()
        if data is None:
            return failure_response(statuscode='400', content='Invalid JSON data in the request')
        required_fields = ['patientEmailId', 'doctorEmailId', 'appointmentDate', 'appointmentTime']
        for field in required_fields:
            if field not in data or not data[field]:
                return failure_response(statuscode='400', content=f'Missing or empty field: {field}')

        doctorEmailId = data['doctorEmailId']
        patientEmailId = data['patientEmailId']
        appointmentDate = data['appointmentDate']
        appointmentTime = data['appointmentTime']
        if check_email_existence(doctorEmailId):
            if check_email_existence(patientEmailId):
                appointmentId=findAppointmnetId(doctorEmailId,patientEmailId,appointmentDate,appointmentTime)
                PMRecordFile=findPMRecord(appointmentId)
                if PMRecordFile:
                    from run import UPLOAD_FOLDER
                    filepath = os.path.join(UPLOAD_FOLDER, PMRecordFile)
                    return send_file(filepath, as_attachment=True)
                else:
                    return failure_response(statuscode='404', content='PMR Record file not found')
            return failure_response(statuscode='409', content=f'EmailId:{doctorEmailId} does not exists')
        return failure_response(statuscode='409', content=f'EmailId:{patientEmailId} does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')
