from app.models.user_model import db


def add_in_entity(new_data):   # To add the datas in the entity
    db.session.add(new_data)
    db.session.commit()

def update_in_entity():   # To edit the datas in the entity
    db.session.commit()

def delete_in_entity(entity):  # To delete the datas in the entity
    db.session.delete(entity)
    db.session.commit()

