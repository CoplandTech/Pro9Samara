from datetime import datetime

from module.TinyDB.config import Query, db_users

def get_user(user_id):
    User = Query()
    return db_users.get(User.id == user_id)

def create_user(user_id, username=None, full_name=None):
    User = Query()
    if not get_user(user_id):
        db_users.insert({
            'id': user_id,
            'username': username or None,
            'full_name': full_name or None,
            'phone_number': None,
            'birth_date': None,
            'date_added': datetime.now().isoformat(),
            'last_active': datetime.now().isoformat(),
        })

def update_user(user_id, **kwargs):
    User = Query()
    db_users.update(kwargs, User.id == user_id)

def is_registration_complete(user_id):
    user = get_user(user_id)
    return user and user.get("phone_number")