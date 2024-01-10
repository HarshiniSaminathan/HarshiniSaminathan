from app.models.employeeModel import db
from app.models.assetModel import db
from app.models.vendorModel import db
from app.models.acceessoriesModel import db
from app.models.assetAssignmentModel import db
from app.models.accessoriesAssModel import db
from app.models.dbModel import db

def add_in_entity(new_data):   # To add the datas in the entity
    db.session.add(new_data)
    db.session.commit()

def update_in_entity():   # To edit the datas in the entity
    db.session.commit()

def delete_in_entity(entity):  # To delete the datas in the entity
    db.session.delete(entity)
    db.session.commit()