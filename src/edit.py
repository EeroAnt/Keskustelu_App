from flask import request, session
from src.db import db
from src.error import error
from sqlalchemy import text
from src.csrf import _csrf_protect
from src.navigation import _return_from_edit


def _edit_header():
    _csrf_protect()
    new_header = request.form["new_header"]
    old_header = request.form["old_header"]
    header_id = request.form["header_id"]
    header_owner = request.form["header_owner"]
    current_user = session["username"]
    if header_owner == current_user:
        sql = "UPDATE headers SET header=:header WHERE id=:header_id"
        db.session.execute(text(sql), {"header_id":int(header_id), "header":new_header})
        sql = "UPDATE messages SET header=:header WHERE header=:old_header"
        db.session.execute(text(sql), {"header":new_header, "old_header":old_header})
        db.session.commit()
    else:
        return error("session_error")
    return _return_from_edit(request.form["topic_id"])


def _edit_message():
    _csrf_protect()
    message = request.form["new_message"]
    message_id = request.form["message_id"]
    message_owner = request.form["message_owner"]
    current_user = session["username"]
    if message_owner == current_user:
        sql = "UPDATE messages SET message=:message WHERE id=:message_id"
        db.session.execute(text(sql), {"message_id":message_id, "message":message})
        db.session.commit()
    else:
        del session["edit"]
        return error("session_error")
    return _return_from_edit(topic_id = request.form["topic_id"],header_id = request.form["header_id"])