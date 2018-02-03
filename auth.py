from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'Thomas', '1234')
]

username_mappings = { u.username: u for u in users }

userid_mappings = { u.id: u for u in users }

def auth(username, password):
    user = username_mappings.get(username, None)
    if user is not None and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mappings.get(user_id, None)
