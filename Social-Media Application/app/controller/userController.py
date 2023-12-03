import datetime
from app.models.userModel import User
from app.models.userProfileModel import UserProfile
from datetime import datetime, timedelta



def check_email_existence(emailid):
    return User.objects(emailid=emailid).first() is not None


def check_username_existence(username):
    return User.objects(username=username,status='ACTIVE').first() is not None

def check_email_For_Username(emailid):
    return User.objects(emailid=emailid,status='ACTIVE').first() is not None

def insert_user(emailid, password, username, fullname, role, status):
    current_time = datetime.utcnow()
    user = User(
        emailid=emailid,
        password=password,
        username=username,
        fullname=fullname,
        role=role,
        status=status,
        created_at=current_time
    )
    user.save()

def check_login(emailid, password):
    try:
        user = User.objects(emailid=emailid, password=password).first()
        return user
    except Exception as e:
        print(f"Error in check_login: {e}")
        return None

def add_profile(emailid,filename,profileName,Bio):
    userprofile = UserProfile(emailid=emailid,profileImage=filename,profileName=profileName,bio=Bio)
    userprofile.save()


def updateSessionCode(emailid, session_code):
    try:
        user = User.objects(emailid=emailid).first()
        if user:
            user.sessionCode = session_code
            user.save()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in updateSessionCode: {e}")
        return False

def check_emailhas_sessionCode(email,session_code):
    return User.objects(emailid=email,sessionCode=session_code).first() is not None

def deleteSession(email):
    try:
        user = User.objects(emailid=email).first()

        if user:
            user.sessionCode = None
            user.save()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in deleteSession: {e}")
        return False
