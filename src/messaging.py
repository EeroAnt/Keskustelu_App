from flask import redirect, request, session
from src.db import db
from src.error import error
from sqlalchemy import text
from src.csrf import csrf_protect


def start_conversation_func(topic_id):
	csrf_protect()
	header = request.form["header"]
	if len(header) > 50:
		return error("header_too_long")
	username = session["username"]
	message = request.form["message"]
	if len(message) > 500:
		return error("message_too_long")
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


def send_message_func(topic_id, header_id):
	csrf_protect()
	message = request.form["message"]
	topic = request.form["topic"]
	username = session["username"]
	header = request.form["header"]
	sql = f"INSERT INTO messages (username, message, time, topic, header) VALUES (:username, :message, NOW(), :topic, :header)"
	db.session.execute(text(sql), {"username":username, "message":message, "topic":topic, "header":header})
	db.session.commit()
	return redirect(f"/topic{topic_id}/conversation{header_id}")