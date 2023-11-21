from app.controller.adminController import findDoctorId
from app.controller.patientController import findPatientId
from app.models.appointmentModel import appointmentTable
from app.utils.commanUtils import update_in_entity


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


