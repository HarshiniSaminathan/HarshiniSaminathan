from sqlalchemy import asc, func

from app.controller.adminController import findDoctorId
from app.controller.patientController import findPatientId
from app.models.appointmentModel import appointmentTable
from app.models.doctorModel import DoctorTable
from app.models.userModel import db, UserTable
from app.utils.commanUtils import update_in_entity
from sqlalchemy.orm import joinedload
from app.models.patientModel import PatientTable
from sqlalchemy import and_, or_


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


def doctor_appointments(doctorEmailId):
    doctor_id = findDoctorId(doctorEmailId)
    current_datetime = datetime.now()
    appointment_status="ACCEPTED"
    appointments = (
        db.session.query(
            PatientTable.patientFirstName,
            PatientTable.patientEmailId,
            PatientTable.patientPhoneNumber,
            appointmentTable.appointmentDate,
            appointmentTable.appointmentTime
        )
        .join(appointmentTable)
        .join(UserTable)
        .filter(appointmentTable.doctorId == doctor_id,appointmentTable.appointmentStatus==appointment_status)
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
            "patientName": patient_name,
            "patientEmailId": patient_email,
            "patientPhoneNumber": patient_phone,
            "appointmentDate": appointment_date.strftime('%Y-%m-%d'),
            "appointmentTime": appointment_time.strftime('%H:%M')
        }
        for patient_name, patient_email, patient_phone, appointment_date, appointment_time in appointments
    ]
    return result


def countOfAppointmentsPerDay(doctorEmailId):
    doctor_id = findDoctorId(doctorEmailId)
    current_date = datetime.now().date()
    counts = (
        db.session.query(
            appointmentTable.appointmentDate,
            func.count().label('appointmentCount')
        )
        .filter(appointmentTable.doctorId == doctor_id)
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