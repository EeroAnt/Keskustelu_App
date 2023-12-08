from flask import session

def is_admin():
	try:
		if session["admin"]:
			return True
	except:
		return False

def is_logged_in():
	try:
		if session["username"]:
			return True
	except:
		return False
