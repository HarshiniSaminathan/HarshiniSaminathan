from app.models.userModel import User

def fetch_inactiveUser_records(page, per_page):

    required_fields = {'username': None, 'emailid': None, 'fullname': None, 'role': None, 'status': None}

    inactive_users = User.objects(status='INACTIVE').only(*required_fields.keys()).paginate(page=page, per_page=per_page)

    total_pages = (inactive_users.total / per_page) + (inactive_users.total % per_page > 0)

    return [{field: getattr(user, field) for field in required_fields} for user in inactive_users.items], int(total_pages)


def activate_user(emailid, status):
    user = User.objects(emailid=emailid).first()
    if user:
        user.status = status
        user.save()

def fetch_active_user_records(page, per_page):

    required_fields = {'username': None, 'emailid': None, 'fullname': None, 'role': None, 'status': None}

    active_users = User.objects(status='ACTIVE').only(*required_fields.keys()).paginate(page=page, per_page=per_page)

    total_pages = (active_users.total / per_page) + (active_users.total % per_page > 0)

    return [{field: getattr(user, field) for field in required_fields} for user in active_users.items], int(total_pages)