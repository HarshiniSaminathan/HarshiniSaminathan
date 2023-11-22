from app.models.patientModel import db
from app.models.adminModel import db
from app.models.appointmentModel import db
from app.models.slotModel import db
from app.models.doctorModel import db
from app.models.medicalRecordsModel import MedicalRecordsTable
from app.models.userModel import db


def add_in_entity(new_data):   # To add the datas in the entity
    db.session.add(new_data)
    db.session.commit()

def update_in_entity():   # To edit the datas in the entity
    db.session.commit()

def delete_in_entity(entity):  # To delete the datas in the entity
    db.session.delete(entity)
    db.session.commit()

