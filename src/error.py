from flask import render_template
from app import app


@app.route("/error")
def error(cause=""):    
    return render_template("error.html", cause=cause)