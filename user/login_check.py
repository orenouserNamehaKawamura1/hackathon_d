from flask import session

def is_login():
    if 'login_ID' not in session:
        return False
    return True