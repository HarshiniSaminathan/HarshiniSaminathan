import base64

from sqlalchemy.orm import joinedload

from app.models.doctorModel import DoctorTable
from app.utils.commanUtils import add_in_entity, update_in_entity
from app.models.userModel import UserTable
from app.models.adminModel import AdminTable
from app.models.slotModel import slotTable
from app.models.feedbackModel import FeedbackSession


def insert_doctor(doctorName, doctorPhoneNumber, doctorAddress, doctorExperience, doctorSpecialization, binary_data,doctorEmailId):
    new_doctor=DoctorTable(
        doctorName=doctorName,
        doctorPhoneNumber=doctorPhoneNumber,
        doctorAddress=doctorAddress,
        doctorExperience=doctorExperience,
        doctorSpecialization=doctorSpecialization,
        doctorSpecializationProof=binary_data,
        doctorEmailId=doctorEmailId
    )
    add_in_entity(new_doctor)


def insert_role_password(EmailId,password,role):
    new_user=UserTable(
        emailId=EmailId,
        password=password,
        role=role
    )
    add_in_entity(new_user)



from flask_sqlalchemy import Pagination

def fetch_doctor_records(page, per_page):
    query = DoctorTable.query
    doctor_info = query.paginate(page=page, per_page=per_page)
    items = doctor_info.items
    if items:
        data = []
        for doctor in items:
            data.append({
                "doctorName": doctor.doctorName,
                "doctorPhoneNumber": doctor.doctorPhoneNumber,
                "doctorAddress": doctor.doctorAddress,
                "doctorExperience": doctor.doctorExperience,
                "doctorSpecialization": doctor.doctorSpecialization,
                "doctorSpecializationProof": base64.b64encode(doctor.doctorSpecializationProof).decode('utf-8'),
                "doctorEmailId": doctor.doctorEmailId
            })

        return data, doctor_info.pages
    else:
        data = [{"data": None}]
        return data


def get_total_doctor():
    total_doctors=DoctorTable.query.count()
    return total_doctors


def insert_admin(adminName, adminPhoneNumber, adminAddress, emailId):
    new_admin=AdminTable(
        adminName=adminName,
        adminPhoneNumber=adminPhoneNumber,
        adminAddress=adminAddress,
        emailId=emailId
    )
    add_in_entity(new_admin)


def fetch_admin_records(page, per_page):
    query = AdminTable.query
    admin_info = query.paginate(page=page, per_page=per_page)
    items = admin_info.items
    if items:
        data = []
        for admin in items:
            data.append({
                "adminName": admin.adminName,
                "adminPhoneNumber": admin.adminPhoneNumber,
                "adminAddress": admin.adminAddress,
                "emailId": admin.emailId
            })

        return data, admin_info.pages
    else:
        data=[{"data":None}]
        return data


def get_total_admin():
    total_admins = AdminTable.query.count()
    return total_admins

def findDoctorId(doctorEmailId):
    found_doctor=DoctorTable.query.filter_by(doctorEmailId=doctorEmailId).first()
    if found_doctor:
        doctorId = found_doctor.doctorId
        return doctorId
    else:
        return None


def insert_slot(doctorEmailId, slotStartTime, slotStatus,slotEndTime):
    doctorId=findDoctorId(doctorEmailId)
    new_slot=slotTable(
        doctorId=doctorId,
        slotStatus=slotStatus,
        slotStartTime=slotStartTime,
        slotEndTime=slotEndTime
    )
    add_in_entity(new_slot)

def check_slot_inserted(doctorEmailId,slotStartTime):
    doctorId = findDoctorId(doctorEmailId)
    existing_slot = slotTable.query.filter_by(doctorId=doctorId, slotStartTime=slotStartTime).first()
    if existing_slot:
        return True
    else:
        return False

def updateSlots(doctorEmailId,slotStartTime, slotEndTime,slotStatus):
    try:
        doctorId = findDoctorId(doctorEmailId)
        slots=slotTable.query.filter_by(doctorId=doctorId,slotStartTime=slotStartTime,slotEndTime=slotEndTime)
        if slots:
            for slot in slots:
                slot.slotStatus = slotStatus
            update_in_entity()
            return True
        else:
            return False
    except Exception as e:
        return False


def addFeedbackResponse(patientId,feedbackTextForAdmin,rating,feedbackResponse):
    try:
        feedback=FeedbackSession.query.filter_by(patientId=patientId,feedbackTextForAdmin=feedbackTextForAdmin,rating=rating)
        if feedback:
            for feeds in feedback:
                feeds.feedbackResponse=feedbackResponse
            update_in_entity()
            return True
        else:
            return False
    except Exception as e:
        return False

def get_feedbacks(page, per_page):
    query = (
        FeedbackSession.query
        .filter(FeedbackSession.feedbackTextForAdmin.isnot(None))
        .options(joinedload(FeedbackSession.patient))
    )

    feedbacks_info = query.paginate(page=page, per_page=per_page)
    feedbacks = feedbacks_info.items
    if feedbacks:
        data_list = []

        for feedback in feedbacks:
            patient = feedback.patient

            data_list.append({
                "patientFirstName": patient.patientFirstName,
                "patientPhoneNumber": patient.patientPhoneNumber,
                "patientEmailId": patient.patientEmailId,
                "feedbacks": feedback.feedbackTextForAdmin,
                "rating": feedback.rating,
                "createdDate": feedback.createdDate,
                "createdTime": feedback.createdTime.strftime('%H:%M'),
                "feedbackResponse": feedback.feedbackResponse
            })

        return data_list, feedbacks_info.pages
    else:
        data=[{"data":None}]
        return data
