from flask import render_template, abort, request, session
from src.db import db
from sqlalchemy import text
from src.querys import _listing_for_index
from src.time_formatter import format_timestamp
from src.clearance import _check_clearance_level


def _index():
    return render_template("index.html", topics=_listing_for_index())


def _go_to_topic(topic_id):
    if _check_clearance_level(topic_id):
        sql = "SELECT topic FROM topics WHERE id=:topic_id"
        result = db.session.execute(text(sql), {"topic_id":topic_id})
        topic = result.fetchone()[0]
        sql = f"SELECT * FROM headers WHERE topic=:topic"
        result = db.session.execute(text(sql), {"topic":topic})
        conversations = result.fetchall()
        return render_template("topic.html", topic=topic, conversations=conversations, topic_id=topic_id)
    else:
        abort(404)


def _go_to_conversation(topic_id, header_id):
    if _check_clearance_level(topic_id):
        topic = db.session.execute(text("SELECT topic FROM topics WHERE id=:topic_id"), {"topic_id":topic_id}).fetchone()[0]
        header = db.session.execute(text("SELECT header FROM headers WHERE id=:header_id"), {"header_id":header_id}).fetchone()[0]
        sql = "SELECT * FROM messages WHERE topic=:topic AND header=:header"
        result = db.session.execute(text(sql), {"topic":topic, "header":header})
        temp_messages = result.fetchall()
        messages = []
        for message in temp_messages:
            messages.append(dict(id=message.id, username=message.username, message=message.message, time=format_timestamp(message.time)))
        return render_template("conversation.html", messages=messages, topic_id=topic_id, header_id=header_id, topic=topic, header=header)
    else:
        abort(404)


def _go_to_edit_message():
    message_id = request.form["message_id"]
    topic_id = request.form["topic_id"]
    header_id = request.form["header_id"]
    session["edit"] = "message"
    sql = "SELECT * FROM messages WHERE id=:message_id"
    message = db.session.execute(text(sql), {"message_id":message_id}).fetchone()
    return render_template("edit.html", message=message, message_id=message_id, topic_id=topic_id, header_id=header_id)


def _go_to_edit_header():
    header_id = request.form["header_id"]
    topic_id = request.form["topic_id"]
    session["edit"] = "header"
    sql = "SELECT * FROM headers WHERE id=:header_id"
    header = db.session.execute(text(sql), {"header_id":int(header_id)}).fetchone()
    return render_template("edit.html", header=header, header_id=header_id, topic_id=topic_id)


def _return_from_edit(topic_id="", header_id=""):
    if session["edit"] == "message":
        del session["edit"]
        return redirect(f"/topic{topic_id}/conversation{header_id}")
    elif session["edit"] == "header":
        del session["edit"]
        return redirect(f"/topic{topic_id}")