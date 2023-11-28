from datetime import datetime

from app.controller.adminController import findDoctorId
from app.models.userModel import UserTable, db
from app.models.appointmentModel import appointmentTable
from app.models.patientModel import PatientTable
from app.utils.commanUtils import update_in_entity


def check_email_existence(emailId):
    count = UserTable.query.filter_by(emailId=emailId).count()
    print(count)
    if count > 0:
        return True
    else:
        return False


def loginVerification(EmailId,password):
    userId = UserTable.query.filter_by(emailId=EmailId, password=password).all()
    return userId


def OldPasswordExists(EmailId,OldPassword):
    userId= UserTable.query.filter_by(emailId=EmailId,password=OldPassword).all()
    if userId:
        return True
    else:
        return False

def change_Password(EmailId,NewPassword):
    try:
        userId=UserTable.query.filter_by(emailId=EmailId).first()
        if userId:
            userId.password=NewPassword
            update_in_entity()
            return True
        else:
            return False
    except Exception as e:
        return False

def updateSessionCode(EmailId,session_code):
    try:
        addSession=UserTable.query.filter_by(emailId=EmailId).first()
        if addSession:
            addSession.sessionCode = session_code
            update_in_entity()
            return True
        else:
            return False
    except Exception as e:
        return False

def deleteSession(email):
    user = UserTable.query.filter_by(emailId=email).first()
    if user:
        user.sessionCode = None
        db.session.commit()
        return True
    return False

def check_emailhas_sessionCode(email,session_code):
    count = UserTable.query.filter_by(emailId=email,sessionCode=session_code).count()
    if count>0:
        return True
    else:
        return False

