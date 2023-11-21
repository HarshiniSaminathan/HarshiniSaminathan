from datetime import datetime

from app.controller.adminController import findDoctorId
from app.models.userModel import UserTable, db
from app.models.appointmentModel import appointmentTable
from app.models.patientModel import PatientTable

def check_email_existence(emailId):
    count = UserTable.query.filter_by(emailId=emailId).count()
    if count > 0:
        return True
    else:
        return False


