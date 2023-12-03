from flask import session

def _is_admin():
    try:
        if session["admin"]:
            return True
    except:
        return False
