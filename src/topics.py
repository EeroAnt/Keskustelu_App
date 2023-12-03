from flask import redirect, request, session
from src.db import db
from src.error import error
from sqlalchemy import text
from src.user_status import _is_admin

def _create():
    if _is_admin():
        topic = request.form["topic"]
        secrecy = request.form["secrecy"]
        check_topic = db.session.execute(text("SELECT Topic FROM topics WHERE Topic=:topic"), {"topic":topic}).fetchone()
        if check_topic:
            return error("topic_error")
        if secrecy == "":
            sql_topics = "INSERT INTO topics (Topic) VALUES (:topic)"
            db.session.execute(text(sql_topics), {"topic":topic})
        else:
            sql_topics = "INSERT INTO topics (Topic, Secrecy) VALUES (:topic, :secrecy)"
            db.session.execute(text(sql_topics), {"topic":topic, "secrecy":secrecy})
        db.session.commit()
    return redirect("/")

def _remove():
    if _is_admin():
        topic = request.form["topic"]
        check_topic = db.session.execute(text("SELECT Topic FROM topics WHERE Topic=:topic"), {"topic":topic}).fetchone()
        if not check_topic:
            return error("topic_not_found_error")
        sql_topics = "DELETE FROM topics WHERE Topic=:topic"
        db.session.execute(text(sql_topics), {"topic":topic})
        sql_headers = "DELETE FROM headers WHERE topic=:topic"
        db.session.execute(text(sql_headers), {"topic":topic})
        sql_messages = "DELETE FROM messages WHERE topic=:topic"
        db.session.execute(text(sql_messages), {"topic":topic})
        db.session.commit()
    return redirect("/")
