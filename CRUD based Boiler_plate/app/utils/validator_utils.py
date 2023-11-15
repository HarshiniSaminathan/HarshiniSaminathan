import re


def is_email_id(email_id):
    try:
        if re.match(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', email_id, re.I):
            return True
        else:
            return False
    except Exception as err:
        return False

def is_valid_password(password):
    try:
        password = str(password)
        if not password:
            return False
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True
    except Exception as err:
        return False

