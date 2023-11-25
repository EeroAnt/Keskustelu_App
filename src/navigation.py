from flask import render_template
from src.db import db
from sqlalchemy import text


def _index():
    sql = "SELECT * FROM topics"
    result = db.session.execute(text(sql))
    topics = result.fetchall()
    return render_template("index.html", topics=topics)


def _go_to_topic(topic_id):
    sql = "SELECT topic FROM topics WHERE id=:topic_id"
    result = db.session.execute(text(sql), {"topic_id":topic_id})
    topic = result.fetchone()[0]
    sql = f"SELECT * FROM headers WHERE topic=:topic"
    result = db.session.execute(text(sql), {"topic":topic})
    conversations = result.fetchall()
    return render_template("topic.html", topic=topic, conversations=conversations, topic_id=topic_id)


def _go_to_conversation(topic_id, header_id):
    topic = db.session.execute(text("SELECT topic FROM topics WHERE id=:topic_id"), {"topic_id":topic_id}).fetchone()[0]
    header = db.session.execute(text("SELECT header FROM headers WHERE id=:header_id"), {"header_id":header_id}).fetchone()[0]
    sql = "SELECT * FROM messages WHERE topic=:topic AND header=:header"
    result = db.session.execute(text(sql), {"topic":topic, "header":header})
    messages = result.fetchall()
    return render_template("conversation.html", messages=messages, topic_id=topic_id, header_id=header_id, topic=topic, header=header)