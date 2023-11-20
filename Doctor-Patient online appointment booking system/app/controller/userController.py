from app.models.userModel import UserTable

def check_email_existence(emailId):
    count = UserTable.query.filter_by(emailId=emailId).count()
    if count > 0:
        return True
    else:
        return False