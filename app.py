from flask import Flask
from flask import redirect, render_template, request, session, flash
from os import getenv
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URI')#"postgresql+psycopg2:///postgres"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if not user:
        return redirect("/login_error")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            if user.admin:
                session["admin"] = True
            session["username"] = username
        else:
            return redirect("/login_error")
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    session["admin"]=False
    return redirect("/")

@app.route("/register", methods=["POST","GET"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    check_username = db.session.execute(text("SELECT username FROM users WHERE username=:username"), {"username":username}).fetchone()
    if check_username:
        return redirect("/register_error")
    sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password , false)"
    db.session.execute(text(sql), {"username":username, "password":hash_value})
    db.session.commit()
    return redirect("/")

@app.route("/create", methods=["POST","GET"])
def create():
    topic = request.form["topic"]
    check_topic = db.session.execute(text("SELECT Topic FROM conversations WHERE Topic=:topic"), {"topic":topic}).fetchone()
    if check_topic:
        return redirect("/topic_error")
    sql_conversations = "INSERT INTO conversations (Topic) VALUES (:topic)"
    db.session.execute(text(sql_conversations), {"topic":topic})
    sql_add = "CREATE TABLE " + topic + " (id SERIAL PRIMARY KEY, username TEXT NOT NULL, message TEXT NOT NULL, time TIMESTAMP NOT NULL)"
    db.session.execute(text(sql_add))
    db.session.commit()
    return redirect("/")

@app.route("/topic_error")
def topic_error():
    return render_template("topic_error.html")

@app.route("/remove", methods=["POST","GET"])
def remove():
    return redirect("/")

@app.route("/login_error")
def error():
    return render_template("login_error.html")

@app.route("/register_error")
def register_error():
    return render_template("register_error.html")