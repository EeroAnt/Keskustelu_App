from flask import session

def _is_admin():
    try:
        if session["admin"]:
            return True
    except:
        return False
    
def _is_logged_in():
    try:
        if session["username"]:
            return True
    except:
        return False
