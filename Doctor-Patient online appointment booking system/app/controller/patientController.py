import datetime

from sqlalchemy import asc, func

from app.controller.adminController import findDoctorId
from app.models.doctorModel import DoctorTable
from app.models.patientModel import PatientTable
from app.models.slotModel import slotTable
from app.models.userModel import db, UserTable
from app.utils.commanUtils import add_in_entity, update_in_entity
from app.models.appointmentModel import appointmentTable
from sqlalchemy import and_, or_
from datetime import datetime


def insert_patient(patientFirstName,patientLastName, patientPhoneNumber,patientDOB,patientAddress,patientEmailId):
    new_patient=PatientTable(
        patientFirstName=patientFirstName,
        patientLastName=patientLastName,
        patientPhoneNumber=patientPhoneNumber,
        patientDOB=patientDOB,
        patientAddress=patientAddress,
        patientEmailId=patientEmailId
    )
    add_in_entity(new_patient)

def fetch_Availabledoctor_records():
    doctorinfo=DoctorTable.query.all()
    data=[]
    for doctor in doctorinfo:
        data.append(
            {
                "doctorName": doctor.doctorName,
                "doctorPhoneNumber": doctor.doctorPhoneNumber,
                "doctorExperience":doctor.doctorExperience,
                "doctorSpecialization" : doctor.doctorSpecialization,
                "doctorEmailId" : doctor.doctorEmailId
            }
        )
    return data


def updateProfile(patientFirstName,patientLastName, patientPhoneNumber,patientDOB,patientAddress,patientEmailId):
    try:
        patient=PatientTable.query.filter_by(patientEmailId=patientEmailId).first()
        if patient:
            patient.patientFirstName = patientFirstName,
            patient.patientLastName = patientLastName,
            patient.patientPhoneNumber=patientPhoneNumber,
            patient.patientDOB=patientDOB,
            patient.patientAddress=patientAddress
            update_in_entity()
            return True
        else:
            return False
    except Exception as e:
        return False


def fetch_slotsfor_doctor(doctorEmailId):
    doctorId = findDoctorId(doctorEmailId)
    if doctorId is None:
        return {"error": "Doctor not found"}
    doctor = DoctorTable.query.get(doctorId)
    if doctor is None:
        return {"error": "Doctor not found"}

    slots = slotTable.query.filter_by(doctorId=doctorId).all()

    data = {
        "doctor": {
            "doctorName": doctor.doctorName,
            "doctorPhoneNumber": doctor.doctorPhoneNumber,
            "doctorExperience": doctor.doctorExperience,
            "doctorSpecialization": doctor.doctorSpecialization,
            "doctorEmailId": doctor.doctorEmailId
        },
        "slots": []
    }

    for slot in slots:
        data["slots"].append(
            {
                "slotStatus": slot.slotStatus,
                "slotStartTime": slot.slotStartTime.strftime("%H:%M"),
                "slotEndTime": slot.slotEndTime.strftime("%H:%M")
            }
        )
    return data


def findPatientId(patientEmailId):
    found_patient=PatientTable.query.filter_by(patientEmailId=patientEmailId).first()
    if found_patient:
        patientId = found_patient.patientId
        return patientId


def requestingAppointmnet(doctorEmailId,appointmentDate, appointmentTime,appointmentStatus,patientEmailId):
    doctorId = findDoctorId(doctorEmailId)
    patientId = findPatientId(patientEmailId)
    new_appointments=appointmentTable(
        doctorId=doctorId,
        appointmentDate=appointmentDate,
        appointmentTime=appointmentTime,
        appointmentStatus=appointmentStatus,
        patientId=patientId
    )
    add_in_entity(new_appointments)

def appointmentNotBooked(doctorEmailId,appointmentDate,appointmentTime):
    doctorId = findDoctorId(doctorEmailId)
    doctor_exists_in_appointments = appointmentTable.query.filter_by(doctorId=doctorId).first()
    if not doctor_exists_in_appointments:
        return True
    appointment = appointmentTable.query.filter_by(
        doctorId=doctorId,
        appointmentDate=appointmentDate,
        appointmentTime=appointmentTime
    ).first()
    if appointment and appointment.appointmentStatus in ["PENDING", "ACCEPTED"]:
        return False
    else:
        return True

def alreadyRequestedForSameDateTime(doctorEmailId,appointmentDate,appointmentTime,patientEmailId):
    doctorId = findDoctorId(doctorEmailId)
    patientId = findPatientId(patientEmailId)
    doctor_exists_in_appointments = appointmentTable.query.filter_by(doctorId=doctorId).first()
    if not doctor_exists_in_appointments:
        return True
    appointment = appointmentTable.query.filter_by(
        doctorId=doctorId,
        appointmentDate=appointmentDate,
        appointmentTime=appointmentTime,
        patientId=patientId
    ).first()
    if appointment and appointment.appointmentStatus in ["REJECTED"]:
        return False
    else:
        return True

def fetch_slotsfor_doctor(doctorEmailId):
    doctorId = findDoctorId(doctorEmailId)
    if doctorId is None:
        return {"error": "Doctor not found"}
    doctor = DoctorTable.query.get(doctorId)
    if doctor is None:
        return {"error": "Doctor not found"}

    slots = slotTable.query.filter_by(doctorId=doctorId).all()

    data = {
        "doctor": {
            "doctorName": doctor.doctorName,
            "doctorPhoneNumber": doctor.doctorPhoneNumber,
            "doctorExperience": doctor.doctorExperience,
            "doctorSpecialization": doctor.doctorSpecialization,
            "doctorEmailId": doctor.doctorEmailId
        },
        "slots": []
    }

    for slot in slots:
        data["slots"].append(
            {
                "slotStatus": slot.slotStatus,
                "slotStartTime": slot.slotStartTime.strftime("%H:%M"),
                "slotEndTime": slot.slotEndTime.strftime("%H:%M")
            }
        )
    return data


def patient_appointments(patientEmailId):
    patient_id = findPatientId(patientEmailId)
    current_datetime = datetime.now()
    appointment_status="ACCEPTED"
    appointments = (
        db.session.query(
            DoctorTable.doctorName,
            DoctorTable.doctorSpecialization,
            DoctorTable.doctorExperience,
            appointmentTable.appointmentDate,
            appointmentTable.appointmentTime
        )
        .join(appointmentTable)
        .join(UserTable)
        .filter(appointmentTable.patientId == patient_id,appointmentTable.appointmentStatus==appointment_status)
        .filter(
            and_(
                appointmentTable.appointmentDate > current_datetime.date(),
                or_(
                    appointmentTable.appointmentDate > current_datetime.date(),
                    and_(
                        appointmentTable.appointmentDate == current_datetime.date(),
                        appointmentTable.appointmentTime > current_datetime.time()
                    )
                )
            )
        )
        .order_by(asc(appointmentTable.appointmentDate), asc(appointmentTable.appointmentTime))
        .all()
    )
    result = [
        {
            "doctorName": doctorName,
            "doctorSpecialization": doctorSpecialization,
            "doctorExperience": doctorExperience,
            "appointmentDate": appointment_date.strftime('%Y-%m-%d'),
            "appointmentTime": appointment_time.strftime('%H:%M')
        }
        for doctorName, doctorSpecialization, doctorExperience, appointment_date, appointment_time in appointments
    ]
    return result


def countOfAppointmentsPerDay(patientEmailId):
    patient_id = findPatientId(patientEmailId)
    current_date = datetime.now().date()
    counts = (
        db.session.query(
            appointmentTable.appointmentDate,
            func.count().label('appointmentCount')
        )
        .filter(appointmentTable.patientId == patient_id)
        .filter(appointmentTable.appointmentStatus == 'ACCEPTED')  # Adjust based on your status criteria
        .filter(appointmentTable.appointmentDate >= current_date)
        .group_by(appointmentTable.appointmentDate)
        .order_by(appointmentTable.appointmentDate)
        .all()
    )

    result = [
        {
            "date": appointment_date.strftime('%Y-%m-%d'),
            "appointmentCount": appointment_count
        }
        for appointment_date, appointment_count in counts
    ]

    return result