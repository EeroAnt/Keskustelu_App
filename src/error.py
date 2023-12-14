from flask import render_template
from app import app


@app.route("/error")
def error(message=""):
	return render_template("error.html", message=message)