from flask import redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from src.db import db
from src.error import error
from sqlalchemy import text

def _login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if not user:
        return error("login_error")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            if user.admin:
                session["admin"] = True
            session["username"] = username
        else:
            return error("login_error")
    return redirect("/")


def _logout():
    del session["username"]
    session["admin"]=False
    return redirect("/")

def _register():
    username = request.form["username"]
    password = request.form["password"]
    admin = request.form["admin"]
    hash_value = generate_password_hash(password)
    if not _check_username(username):
        return error("register_error")
    if admin == '1':
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password , true)"
    else:
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password , false)"
    db.session.execute(text(sql), {"username":username, "password":hash_value})
    db.session.commit()
    return redirect("/")

def _check_username(username):
    check_username = db.session.execute(text("SELECT username FROM users WHERE username=:username"), {"username":username}).fetchone()
    if check_username:
        return True
    else:
        return False