import base64
import math
from datetime import datetime, timedelta
import datetime

from flask import jsonify
from sqlalchemy import asc, func

from app.controller.adminController import findDoctorId
from app.models.doctorModel import DoctorTable
from app.models.patientModel import PatientTable
from app.models.slotModel import slotTable
from app.models.userModel import db, UserTable
from app.models.medicalRecordsModel import MedicalRecordsTable, PMRecordTable
from app.utils.commanUtils import add_in_entity, update_in_entity
from app.models.appointmentModel import appointmentTable
from app.models.prescriptionModel import PrescriptionTable
from sqlalchemy import and_, or_
from datetime import datetime
from app.models.feedbackModel import FeedbackSession



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

def fetch_Availabledoctor_records(page, per_page):
    doctor_query = DoctorTable.query
    doctor_info_paginated = doctor_query.paginate(page=page, per_page=per_page)
    doctor_info = doctor_info_paginated.items
    data = []
    if doctor_info:
        for doctor in doctor_info:
            data.append(
                {
                    "doctorName": doctor.doctorName,
                    "doctorPhoneNumber": doctor.doctorPhoneNumber,
                    "doctorExperience": doctor.doctorExperience,
                    "doctorSpecialization": doctor.doctorSpecialization,
                    "doctorEmailId": doctor.doctorEmailId
                }
            )

        return data, doctor_info_paginated.pages
    else:
        return [{"data": None}]



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

def fetch_slotsfor_doctor(doctorEmailId,):
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


from sqlalchemy import func

def patient_appointments(patientEmailId, page, per_page):
    patient_id = findPatientId(patientEmailId)
    current_datetime = datetime.now()
    appointment_status = "ACCEPTED"

    query = (
        db.session.query(
            DoctorTable.doctorName,
            DoctorTable.doctorSpecialization,
            DoctorTable.doctorExperience,
            appointmentTable.appointmentDate,
            appointmentTable.appointmentTime
        )
        .join(appointmentTable)
        .join(UserTable)
        .filter(appointmentTable.patientId == patient_id, appointmentTable.appointmentStatus == appointment_status)
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
    )

    total_records = query.count()

    appointments = query.offset((page - 1) * per_page).limit(per_page).all()

    if appointments:
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
        return result, total_records
    else:
        return [{"data": None}]



def countOfAppointmentsPerDay(patientEmailId, page, per_page):
    patient_id = findPatientId(patientEmailId)
    current_date = datetime.now().date()

    query = (
        db.session.query(
            appointmentTable.appointmentDate,
            func.count().label('appointmentCount')
        )
        .filter(appointmentTable.patientId == patient_id)
        .filter(appointmentTable.appointmentStatus == 'ACCEPTED')
        .filter(appointmentTable.appointmentDate >= current_date)
        .group_by(appointmentTable.appointmentDate)
        .order_by(appointmentTable.appointmentDate)
    )

    total_records = query.count()

    appointments = query.offset((page - 1) * per_page).limit(per_page).all()
    if appointments:
        result = [
            {
                "date": appointment_date.strftime('%Y-%m-%d'),
                "appointmentCount": appointment_count
            }
            for appointment_date, appointment_count in appointments
        ]

        return result, total_records
    else:
        return [{"data": None}]


def doctorForSpecialization_exists(doctorSpecialization):
    count=DoctorTable.query.filter_by(doctorSpecialization=doctorSpecialization).count()
    if count>0:
        return True
    else:
        return False


def doctor_for_Specialization(doctorSpecialization, page, per_page):
    doctors = (
        DoctorTable.query
        .filter_by(doctorSpecialization=doctorSpecialization)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    data = []
    if doctors:
        for doctor in doctors:
            data.append({
                "doctorName": doctor.doctorName,
                "doctorPhoneNumber": doctor.doctorPhoneNumber,
                "doctorExperience": doctor.doctorExperience,
                "doctorSpecialization": doctor.doctorSpecialization,
                "doctorEmailId": doctor.doctorEmailId
            })

        total_records = DoctorTable.query.filter_by(doctorSpecialization=doctorSpecialization).count()
        total_pages = math.ceil(total_records / per_page)
        return data,total_pages
    else:
        return [{"data": None}]

def check_for_slotsPending(doctorEmailId,appointmentDate):
    doctorId=findDoctorId(doctorEmailId)
    pending_and_rejected_slots = (
        appointmentTable.query
        .filter(
            appointmentTable.doctorId == doctorId,
            appointmentTable.appointmentDate == appointmentDate,
            appointmentTable.appointmentStatus == 'PENDING'
        )
        .all()
    )
    if pending_and_rejected_slots:
        data=[]
        for slots in pending_and_rejected_slots:
            data.append(
                {
                    "appointmentTime": slots.appointmentTime.strftime('%H:%M')
                }
            )
        return data
    else:
        return [{"data": None}]


def check_for_slotsRejected(doctorEmailId,appointmentDate):
    doctorId=findDoctorId(doctorEmailId)
    pending_and_rejected_slots = (
        appointmentTable.query
        .filter(
            appointmentTable.doctorId == doctorId,
            appointmentTable.appointmentDate == appointmentDate,
            appointmentTable.appointmentStatus == 'REJECTED'
        )
        .all()
    )
    data=[]
    if pending_and_rejected_slots:
        for slots in pending_and_rejected_slots:
            data.append(
                {
                    "appointmentTime": slots.appointmentTime.strftime('%H:%M')
                }
            )
        return data
    else:
        return [{"data": None}]


def check_for_slotsNotRequested(doctorEmailId,appointmentDate):
    doctorId = findDoctorId(doctorEmailId)
    slottiming=slotTable.query.filter_by(doctorId=doctorId)
    data=[]
    if slottiming:
        for timimg in slottiming:
            slotStartTime=timimg.slotStartTime.strftime('%H:%M')
            data.append(slotStartTime)
        print("slots in slot table",data)
        Timeforappointment=appointmentTable.query.filter_by(doctorId=doctorId,appointmentDate=appointmentDate)

        TimeInappointment=[]
        if Timeforappointment:
            for time in Timeforappointment:
                appointmenttime=time.appointmentTime.strftime('%H:%M')
                TimeInappointment.append(appointmenttime)

            print("appoinmenttime in appointment table",TimeInappointment)
            not_requested=[]
            for slottime in data:
                if slottime not in TimeInappointment:
                    not_requested.append({
                            "appointmentTime":slottime
                        })
            print("not requested appointment",not_requested)
            return not_requested
        else:
            return [{"data": None}]
    else:
        return [{"data": None}]

def check_appointmentAccepted(doctorEmailId,patientEmailId,appointmentDate,appointmentTime):
    appointmentStatus="ACCEPTED"
    doctorId=findDoctorId(doctorEmailId)
    patientId=findPatientId(patientEmailId)
    count=appointmentTable.query.filter_by(doctorId=doctorId,patientId=patientId,appointmentStatus=appointmentStatus,appointmentDate=appointmentDate,appointmentTime=appointmentTime).count()
    print(count)
    if count >0:
        return True
    else:
        return False


def findAppointmnetId(doctorEmailId,patientEmailId,appointmentDate,appointmentTime):
    doctorId=findDoctorId(doctorEmailId)
    patientId=findPatientId(patientEmailId)
    appointmentStatus = "ACCEPTED"
    appointment=appointmentTable.query.filter_by(doctorId=doctorId,patientId=patientId,appointmentDate=appointmentDate,appointmentTime=appointmentTime,appointmentStatus=appointmentStatus).first()
    if appointment:
        appointmentID=appointment.appointmentId
        print(appointmentID)
        return appointmentID

def addPMReport(appointmentId,PMReport,description):
    current_time = datetime.now().strftime('%H:%M')
    current_date = datetime.now().strftime('%Y-%m-%d')
    new_report=MedicalRecordsTable(
        appointmentId=appointmentId,
        PMReport=PMReport,
        description=description,
        createdDate=current_date,
        createdTime=current_time
    )
    add_in_entity(new_report)

def add_filePMReport(appointmentId,filename,description):
    current_time = datetime.now().strftime('%H:%M')
    current_date = datetime.now().strftime('%Y-%m-%d')
    new_report=PMRecordTable(
        appointmentId=appointmentId,
        PMReport=filename,
        description=description,
        createdDate=current_date,
        createdTime=current_time
    )
    add_in_entity(new_report)


def prescription_datas(appointmentId, page, per_page):
    query = PrescriptionTable.query.filter_by(appointmentId=appointmentId)
    prescription_info = query.paginate(page=page, per_page=per_page)
    items = prescription_info.items
    if items:
        data = []
        for datas in items:
            data.append(
                {
                    "medication": datas.medication,
                    "dosage": datas.dosage,
                    "instruction": datas.instruction,
                    "createdDate": datas.createdDate.strftime('%Y-%m-%d'),
                    "createdTime": datas.createdTime.strftime('%H:%M')
                }
            )
        total_pages = prescription_info.pages

        return data,total_pages
    else:
        return {"data": [{"data": None}], "total_pages": 0}

def add_Feedback_To_Doctor(patientEmailId,doctorEmailId,feedbackText,rating):
    patientId=findPatientId(patientEmailId)
    doctorId=findDoctorId(doctorEmailId)
    current_time = datetime.now().strftime('%H:%M')
    current_date = datetime.now().strftime('%Y-%m-%d')
    new_feedback =  FeedbackSession(
        patientId=patientId,
        doctorId=doctorId,
        feedbackTextForDoctor=feedbackText,
        rating=rating,
        createdDate=current_date,
        createdTime=current_time
    )
    add_in_entity(new_feedback)

def add_Feedback_To_Admin(patientEmailId, feedbackText, rating):
    patientId = findPatientId(patientEmailId)
    current_time = datetime.now().strftime('%H:%M')
    current_date = datetime.now().strftime('%Y-%m-%d')
    new_feedback =  FeedbackSession(
        patientId=patientId,
        feedbackTextForAdmin=feedbackText,
        rating=rating,
        createdDate=current_date,
        createdTime=current_time
    )
    add_in_entity(new_feedback)


def get_Prescription(patientEmailId, doctorEmailId, page, per_page):
    patient_id = findPatientId(patientEmailId)
    doctor_id = findDoctorId(doctorEmailId)
    appointment_status = "ACCEPTED"
    appointments_query = (
        db.session.query(
            DoctorTable.doctorName,
            DoctorTable.doctorSpecialization,
            DoctorTable.doctorEmailId,
            appointmentTable.appointmentDate,
            appointmentTable.appointmentTime
        )
        .join(appointmentTable)
        .join(UserTable)
        .filter(appointmentTable.doctorId == doctor_id, appointmentTable.appointmentStatus == appointment_status, appointmentTable.patientId == patient_id)
        .order_by(asc(appointmentTable.appointmentDate), asc(appointmentTable.appointmentTime))
    )

    appointments = appointments_query.paginate(page=page, per_page=per_page)

    items = appointments.items
    if items:
        result = []
        for doctorName, doctorSpecialization, doctorEmailId, appointment_date, appointment_time in items:
            appointmentId = findAppointmnetId(doctorEmailId, patientEmailId, appointment_date, appointment_time)
            prescription_records = PrescriptionTable.query.filter_by(appointmentId=appointmentId).all()

            prescription_for_appointment = []
            if prescription_records:
                for medical_record in prescription_records:
                    medication = medical_record.medication
                    dosage = medical_record.dosage
                    instruction = medical_record.dosage

                    prescription_for_appointment.append({
                        "medication": medication,
                        "dosage": dosage,
                        "instruction": instruction
                    })

                result.append({
                    "doctorName": doctorName,
                    "doctorEmailId": doctorEmailId,
                    "doctorSpecialization": doctorSpecialization,
                    "appointmentDate": appointment_date.strftime('%Y-%m-%d'),
                    "appointmentTime": appointment_time.strftime('%H:%M'),
                    "medicalRecords": prescription_for_appointment
                })

        total_pages = appointments.pages

        return result,total_pages
    else:
        return {"data": [{"data": None}], "total_pages": 0}

def check_for_PMR_beforeDay():
    try:
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        date_of_tomorrow = tomorrow.date()

        appointments = (
            appointmentTable.query
            .filter_by(appointmentDate=date_of_tomorrow)
            .all()
        )
        if appointments:
            patient_email_ids = []
            for record in appointments:
                appointment_id = record.appointmentId
                checkInPMRtable=PMRecordTable.query.filter_by(appointmentId=appointment_id).all()
                if not checkInPMRtable:
                    patient_ids = appointmentTable.query.filter_by(appointmentId=appointment_id).all()
                    for appointment in patient_ids:
                        patient_id = appointment.patientId
                        patient_email = PatientTable.query.filter_by(patientId=patient_id).first()
                        if patient_email:
                            patient_email_ids.append(patient_email.patientEmailId)
            for email_id in patient_email_ids:
                from app.utils.emailSender import send_email
                send_email(email_id)
                return jsonify({'message':  f'{email_id}'})

            return jsonify({'message': 'All PMR reports are added for tomorrow'})

        else:
            return jsonify({'message': 'No appointments for tomorrow'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': f'{e}'})










