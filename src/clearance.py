from flask import request, session, redirect
from src.db import db
from sqlalchemy import text
from src.error import error
from src.login import _check_username

def _give_clearance():
    if session["admin"]:
        user = request.form["user"]
        clearance_level = request.form["clearance_level"]
        if _check_username(user):
            sql = "INSERT INTO clearances (username, level) VALUES (:user, :clearance_level)"
            db.session.execute(text(sql), {"user":user, "clearance_level":clearance_level})
            db.session.commit()
        else:
            return error("no_user")
    return redirect("/")