from flask import redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from src.db import db
from src.error import error
from sqlalchemy import text
from secrets import token_hex
from src.user_status import is_admin


def login_func():
	username = request.form["username"]
	password = request.form["password"]
	session["csrf_token"] = token_hex(16)
	sql = "SELECT id, password, admin FROM users WHERE username=:username"
	result = db.session.execute(text(sql), {"username":username})
	user = result.fetchone()
	if not user:
		return error("Käyttäjää ei ole olemassa")
	else:
		hash_value = user.password
		if check_password_hash(hash_value, password):
			if user.admin:
				session["admin"] = True
			session["username"] = username
		else:
			return error("Käyttäjänimi ja salasana eivät täsmää")
	return redirect("/")


def logout_func():
	del session["username"]
	del session["csrf_token"]
	if is_admin():
		del session["admin"]
	return redirect("/")

def register_func():
	username = request.form["username"]
	password = request.form["password"]
	admin = request.form["admin"]
	hash_value = generate_password_hash(password)
	if check_username(username):
		return error("Käyttäjänimi ei ole käytettävissä")
	if admin == '1':
		sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password , true)"
	else:
		sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password , false)"
	db.session.execute(text(sql), {"username":username, "password":hash_value})
	db.session.commit()
	return redirect("/")

def check_username(username):
	check_username = db.session.execute(text("SELECT username FROM users WHERE username=:username"), {"username":username}).fetchone()
	if check_username:
		return True
	else:
		return False