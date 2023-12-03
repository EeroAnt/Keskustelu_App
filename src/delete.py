from flask import redirect, request, session
from src.db import db
from src.error import error
from sqlalchemy import text
from src.csrf import _csrf_protect
from src.admin import _is_admin

def _remove_message():
    _csrf_protect()
    message_id = request.form["message_id"]
    current_user = session["username"]
    message_owner = request.form["message_owner"]
    topic_id = request.form["topic_id"]
    header_id = request.form["header_id"]
    if message_owner == current_user or _is_admin():
        sql = "DELETE FROM messages WHERE id=:message_id"
        db.session.execute(text(sql), {"message_id":message_id})
        db.session.commit()
    else:
        return error("session_error")
    return redirect(f"/topic{topic_id}/conversation{header_id}")


def _remove_conversation():
    _csrf_protect()
    header_id = request.form["header_id"]
    current_user = session["username"]
    header_owner = request.form["header_owner"]
    topic_id = request.form["topic_id"]
    header = db.session.execute(text("SELECT header FROM headers WHERE id=:header_id"), {"header_id":header_id}).fetchone()[0]
    topic = db.session.execute(text("SELECT topic FROM topics WHERE id=:topic_id"), {"topic_id":topic_id}).fetchone()[0]
    if header_owner == current_user or _is_admin():
        sql = "DELETE FROM headers WHERE id=:header_id"
        db.session.execute(text(sql), {"header_id":int(header_id)})
        sql = "DELETE FROM messages WHERE header=:header and topic=:topic"
        db.session.execute(text(sql), {"header":header, "topic":topic})
        db.session.commit()
    else:
        return error("session_error")
    return redirect(f"/topic{topic_id}")