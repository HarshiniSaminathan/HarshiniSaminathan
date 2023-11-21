from flask import request

from app.controller.userController import check_email_existence
from app.response import failure_response, success_response
from app.controller.doctorController import respondingAppointments

def responding_for_appointment(doctorEmailId):
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
                return success_response(f'Appointment Responded as : {appointmentStatus}')
            return failure_response(statuscode='409', content='Email id does not exists')
        return failure_response(statuscode='409', content='Email id does not exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content='An unexpected error occurred.')