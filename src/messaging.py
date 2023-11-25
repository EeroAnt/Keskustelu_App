from flask import redirect, request, session
from src.db import db
from src.error import error
from sqlalchemy import text

def _start_conversation(topic_id):
    header = request.form["header"]
    username = session["username"]
    message = request.form["message"]
    topic = request.form["topic"]
    check_header = db.session.execute(text(f"SELECT header FROM headers WHERE header=:header AND topic=:topic"), {"header":header,"topic":topic}).fetchone()
    if check_header:
        return error("header_error")
    sql = f"INSERT INTO headers (username, header, topic) VALUES (:username, :header, :topic)"
    db.session.execute(text(sql), {"username":username, "header":header, "topic":topic})
    sql = f"INSERT INTO messages (username, message, time, header, topic) VALUES (:username, :message, NOW(), :header, :topic)"
    db.session.execute(text(sql), {"username":username, "message":message, "header":header, "topic":topic})    
    db.session.commit()
    return redirect(f"/topic{topic_id}")


def _send_message(topic_id, header_id):
    message = request.form["message"]
    topic = request.form["topic"]
    username = session["username"]
    header = request.form["header"]
    sql = f"INSERT INTO messages (username, message, time, topic, header) VALUES (:username, :message, NOW(), :topic, :header)"
    db.session.execute(text(sql), {"username":username, "message":message, "topic":topic, "header":header})
    db.session.commit()
    return redirect(f"/topic{topic_id}/conversation{header_id}")