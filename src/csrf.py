from flask import session, abort, request

def csrf_protect():
	if session["csrf_token"] != request.form["csrf_token"]:
		abort(403)