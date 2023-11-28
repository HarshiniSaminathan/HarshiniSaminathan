import base64
import os

from sqlalchemy import asc, func

from app.controller.adminController import findDoctorId
from app.controller.patientController import findPatientId, findAppointmnetId
from app.models.appointmentModel import appointmentTable
from app.models.doctorModel import DoctorTable
from app.models.feedbackModel import FeedbackSession
from app.models.userModel import db, UserTable
from app.utils.commanUtils import update_in_entity, add_in_entity
from sqlalchemy.orm import joinedload
from app.models.patientModel import PatientTable
from sqlalchemy import and_, or_
from app.models.medicalRecordsModel import MedicalRecordsTable, PMRecordTable
from app.models.prescriptionModel import PrescriptionTable


from datetime import datetime




def respondingAppointments(doctorEmailId, appointmentDate, appointmentTime, appointmentStatus, patientEmailId):
    try:
        doctorId = findDoctorId(doctorEmailId)
        patientId = findPatientId(patientEmailId)
        appointment = appointmentTable.query.filter_by(
            doctorId=doctorId,
            appointmentDate=appointmentDate,
            appointmentTime=appointmentTime,
            patientId=patientId
        ).first()
        if appointment:
            appointment.appointmentStatus = appointmentStatus
            update_in_entity()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def countOfAppointmentsPerDay(doctorEmailId, page, per_page):
    doctor_id = findDoctorId(doctorEmailId)
    current_date = datetime.now().date()
    counts_query = (
        db.session.query(
            appointmentTable.appointmentDate,
            func.count().label('appointmentCount')
        )
        .filter(appointmentTable.doctorId == doctor_id)
        .filter(appointmentTable.appointmentStatus == 'ACCEPTED')
        .filter(appointmentTable.appointmentDate >= current_date)
        .group_by(appointmentTable.appointmentDate)
        .order_by(appointmentTable.appointmentDate)
    )
    counts_info = counts_query.paginate(page=page, per_page=per_page)
    counts = counts_info.items

    result = [
        {
            "date": appointment_date.strftime('%Y-%m-%d'),
            "appointmentCount": appointment_count
        }
        for appointment_date, appointment_count in counts
    ]
    return result, counts_info.pages

def doctor_appointments(doctorEmailId, page, per_page):
    doctor_id = findDoctorId(doctorEmailId)
    current_datetime = datetime.now()
    appointment_status = "ACCEPTED"
    appointments_query = (
        db.session.query(
            PatientTable.patientFirstName,
            PatientTable.patientEmailId,
            PatientTable.patientPhoneNumber,
            appointmentTable.appointmentDate,
            appointmentTable.appointmentTime
        )
        .join(appointmentTable)
        .join(UserTable)
        .filter(appointmentTable.doctorId == doctor_id, appointmentTable.appointmentStatus == appointment_status)
        .filter(
            and_(
                appointmentTable.appointmentDate > current_datetime.date(),
                or_(
                    appointmentTable.appointmentDate > current_datetime.date(),
                    and_(
                        appointmentTable.appointmentDate == current_datetime.date(),
                        appointmentTable.appointmentTime > current_datetime.time()
                    ))))
        .order_by(asc(appointmentTable.appointmentDate), asc(appointmentTable.appointmentTime))
    )

    appointments_info = appointments_query.paginate(page=page, per_page=per_page)
    appointments = appointments_info.items
    if appointments:
        result = []
        for patient_name, patient_email, patient_phone, appointment_date, appointment_time in appointments:
            appointmentId = findAppointmnetId(doctorEmailId, patient_email, appointment_date, appointment_time)
            print(appointmentId)
            medical_records = PMRecordTable.query.filter_by(appointmentId=appointmentId).first()

            records_for_appointment = []
            if medical_records:
                PMReport = medical_records.PMReport
                description = medical_records.description
                records_for_appointment.append({
                    "PMReport": PMReport,
                    "description": description
                        })
                print(records_for_appointment)
            else:
                records_for_appointment.append({
                    "PMReport": None,
                    "description": None
                })

            result.append({
                "patientName": patient_name,
                "patientEmailId": patient_email,
                "patientPhoneNumber": patient_phone,
                "appointmentDate": appointment_date.strftime('%Y-%m-%d'),
                "appointmentTime": appointment_time.strftime('%H:%M'),
                "medicalRecords": records_for_appointment
                })
        return result, appointments_info.pages
    else:
        return None



def addPrescription(appointmentId, medication, dosage,instruction):
    current_time = datetime.now().strftime('%H:%M')
    current_date = datetime.now().strftime('%Y-%m-%d')
    new_Prescription=PrescriptionTable(
        appointmentId=appointmentId,
        medication=medication,
        dosage=dosage,
        instruction=instruction,
        createdDate=current_date,
        createdTime=current_time
    )
    add_in_entity(new_Prescription)


def addFeedbackResponse(patientId,feedbackTextForDoctor,rating,feedbackResponse,doctorId):
    try:
        feedback=FeedbackSession.query.filter_by(patientId=patientId,doctorId=doctorId,feedbackTextForDoctor=feedbackTextForDoctor,rating=rating)
        if feedback:
            for feeds in feedback:
                feeds.feedbackResponse=feedbackResponse
            update_in_entity()
            return True
        else:
            return False
    except Exception as e:
        return False


def get_feedbacks(doctorEmailId, page, per_page):
    doctor_id = findDoctorId(doctorEmailId)
    feedbacks_query = (
        FeedbackSession.query
        .filter_by(doctorId=doctor_id)
        .options(joinedload(FeedbackSession.patient))
    )
    feedbacks_info = feedbacks_query.paginate(page=page, per_page=per_page)
    feedbacks = feedbacks_info.items

    if feedbacks:
        data_list = []
        for feedback in feedbacks:
            patient = feedback.patient

            data_list.append({
                "patientFirstName": patient.patientFirstName,
                "patientPhoneNumber": patient.patientPhoneNumber,
                "patientEmailId": patient.patientEmailId,
                "feedbacks": feedback.feedbackTextForDoctor,
                "rating": feedback.rating,
                "createdDate": feedback.createdDate,
                "createdTime": feedback.createdTime.strftime('%H:%M'),
                "feedbackResponse": feedback.feedbackResponse
            })
        return data_list, feedbacks_info.pages
    else:
        return [{"data": None}]



def get_patient_PMReports(patientEmailId, doctorEmailId, page, per_page):
    patient_id = findPatientId(patientEmailId)
    doctor_id = findDoctorId(doctorEmailId)
    appointment_status = "ACCEPTED"
    appointments_query = (
        db.session.query(
            PatientTable.patientFirstName,
            PatientTable.patientEmailId,
            PatientTable.patientPhoneNumber,
            appointmentTable.appointmentDate,
            appointmentTable.appointmentTime
        )
        .join(appointmentTable)
        .join(UserTable)
        .filter(
            appointmentTable.doctorId == doctor_id,
            appointmentTable.appointmentStatus == appointment_status,
            appointmentTable.patientId == patient_id
        )
        .order_by(asc(appointmentTable.appointmentDate), asc(appointmentTable.appointmentTime))
    )
    appointments_info = appointments_query.paginate(page=page, per_page=per_page)
    appointments = appointments_info.items

    if appointments:
        result = []
        for patient_name, patient_email, patient_phone, appointment_date, appointment_time in appointments:
            appointmentId = findAppointmnetId(doctorEmailId, patient_email, appointment_date, appointment_time)
            medical_records = PMRecordTable.query.filter_by(appointmentId=appointmentId).all()

            records_for_appointment = []
            for medical_record in medical_records:
                PMReport = medical_record.PMReport
                description = medical_record.description
                from run import UPLOAD_FOLDER
                records_for_appointment.append({
                    "PMReport": PMReport,
                    "file_path": os.path.join(UPLOAD_FOLDER, PMReport),
                    "description": description
                })

            result.append({
                "patientName": patient_name,
                "patientEmailId": patient_email,
                "patientPhoneNumber": patient_phone,
                "appointmentDate": appointment_date.strftime('%Y-%m-%d'),
                "appointmentTime": appointment_time.strftime('%H:%M'),
                "medicalRecords": records_for_appointment
            })

        return result, appointments_info.pages
    else:
        return [{"data": None}]


def findPMRecord(appointmentId):
    PMRfile=PMRecordTable.query.filter_by(appointmentId=appointmentId).first()
    if PMRfile:
        PMRfiles=PMRfile.PMReport
        return PMRfiles
    else:
        return None