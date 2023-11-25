from flask import redirect, render_template, request, session
from src.db import db
from src.error import error
from sqlalchemy import text


def _go_to_edit_header():
    header_id = request.form["header_id"]
    topic_id = request.form["topic_id"]
    session["edit"] = "header"
    sql = "SELECT * FROM headers WHERE id=:header_id"
    header = db.session.execute(text(sql), {"header_id":int(header_id)}).fetchone()
    return render_template("edit.html", header=header, header_id=header_id, topic_id=topic_id)


def _edit_header():
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


def _go_to_edit_message():
    message_id = request.form["message_id"]
    topic_id = request.form["topic_id"]
    header_id = request.form["header_id"]
    session["edit"] = "message"
    sql = "SELECT * FROM messages WHERE id=:message_id"
    message = db.session.execute(text(sql), {"message_id":message_id}).fetchone()
    return render_template("edit.html", message=message, message_id=message_id, topic_id=topic_id, header_id=header_id)


def _edit_message():
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


def _return_from_edit(topic_id="", header_id=""):
    if session["edit"] == "message":
        del session["edit"]
        return redirect(f"/topic{topic_id}/conversation{header_id}")
    elif session["edit"] == "header":
        del session["edit"]
        return redirect(f"/topic{topic_id}")