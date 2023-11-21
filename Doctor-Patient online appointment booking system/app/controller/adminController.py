import base64

from app.models.doctorModel import DoctorTable
from app.utils.commanUtils import add_in_entity, update_in_entity
from app.models.userModel import UserTable
from app.models.adminModel import AdminTable
from app.models.slotModel import slotTable


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


def fetch_doctor_records():
    doctorinfo=DoctorTable.query.all()
    data=[]
    for doctor in doctorinfo:
        data.append(
            {
                "doctorName": doctor.doctorName,
                "doctorPhoneNumber": doctor.doctorPhoneNumber,
                "doctorAddress": doctor.doctorAddress,
                "doctorExperience":doctor.doctorExperience,
                "doctorSpecialization" : doctor.doctorSpecialization,
                "doctorSpecializationProof" :doctor.doctorSpecializationProof,
                "doctorEmailId" : doctor.doctorEmailId
            }
        )
    for doctor in data:
        if 'doctorSpecializationProof' in doctor:
            doctor['doctorSpecializationProof'] = base64.b64encode(doctor['doctorSpecializationProof']).decode('utf-8')
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


def fetch_admin_records():
    admininfo=AdminTable.query.all()
    data=[]
    for admin in admininfo:
        data.append(
            {
                "adminName" :admin.adminName,
                "adminPhoneNumber" : admin.adminPhoneNumber,
                "adminAddress" : admin.adminAddress,
                "emailId" : admin.emailId
            }
        )
    return data


def get_total_admin():
    total_admins = AdminTable.query.count()
    return total_admins

def findDoctorId(doctorEmailId):
    found_doctor=DoctorTable.query.filter_by(doctorEmailId=doctorEmailId).first()
    if found_doctor:
        doctorId = found_doctor.doctorId
        return doctorId


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
