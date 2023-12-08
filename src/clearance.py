from flask import request, session, redirect, abort
from src.db import db
from sqlalchemy import text
from src.error import error
from src.login import _check_username
from src.user_status import _is_admin, _is_logged_in

def _give_clearance():
	if _is_admin():
		user = request.form["user"]
		clearance_level = request.form["clearance_level"]
		if _check_username(user):
			sql = "INSERT INTO clearances (username, level) VALUES (:user, :clearance_level)"
			db.session.execute(text(sql), {"user":user, "clearance_level":clearance_level})
			db.session.commit()
		else:
			return error("no_user")
	return redirect("/")

def _check_clearance_level(topic_id):
	if _is_admin():
		return True
	if not _is_logged_in():
		abort(404)
	sql1 = "SELECT topic FROM topics WHERE id=:topic_id"
	topic = db.session.execute(text(sql1), {"topic_id":topic_id}).fetchone()[0]
	sql2 = "SELECT secrecy FROM topics WHERE topic=:topic"
	secrecy = db.session.execute(text(sql2), {"topic":topic}).fetchone()[0]
	if secrecy == None:
		return True
	user = session["username"]
	sql3 = f"SELECT level FROM clearances WHERE username='{user}' AND level={secrecy}"
	if db.session.execute(text(sql3), {"topic":topic}).fetchone() != None:
		return True
	return False
