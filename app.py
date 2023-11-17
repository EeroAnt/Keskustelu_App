from flask import Flask
from flask import redirect, render_template, request, session, flash
from os import getenv
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URI')
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT * FROM conversations"
    result = db.session.execute(text(sql))
    topics = result.fetchall()
    return render_template("index.html", topics=topics)


@app.route("/conversation/<int:id>")
def go_to_conversation(id):
    sql = "SELECT topic FROM conversations WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    topic = result.fetchone()[0]
    sql = f"SELECT * FROM {topic}"
    result = db.session.execute(text(sql))
    messages = result.fetchall()
    return render_template("conversation.html", topic=topic, messages=messages, id=id)



@app.route("/conversation/<int:id>/message", methods=["POST","GET"])
def send_message(id):
    message = request.form["message"]
    topic = request.form["topic"]
    username = session["username"]
    sql = f"INSERT INTO {topic} (username, message, time) VALUES (:username, :message, NOW())"
    db.session.execute(text(sql), {"username":username, "message":message})
    db.session.commit()
    return redirect(f"/conversation/{id}")


@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if not user:
        session["error"]="login_error"
        return redirect("/error")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            if user.admin:
                session["admin"] = True
            session["username"] = username
        else:
            session["error"]="login_error"
            return redirect("/error")
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
        session["error"]="register_error"
        return redirect("/error")
    sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password , false)"
    db.session.execute(text(sql), {"username":username, "password":hash_value})
    db.session.commit()
    return redirect("/")


@app.route("/create", methods=["POST","GET"])
def create():
    topic = request.form["topic"]
    check_topic = db.session.execute(text("SELECT Topic FROM conversations WHERE Topic=:topic"), {"topic":topic}).fetchone()
    if check_topic:
        session["error"]="topic_error"
        return redirect("/error")
    sql_conversations = "INSERT INTO conversations (Topic) VALUES (:topic)"
    db.session.execute(text(sql_conversations), {"topic":topic})
    sql_add = "CREATE TABLE " + topic + " (id SERIAL PRIMARY KEY, username TEXT NOT NULL, message TEXT NOT NULL, time TIMESTAMP NOT NULL)"
    db.session.execute(text(sql_add))
    db.session.commit()
    return redirect("/")


@app.route("/remove", methods=["POST","GET"])
def remove():
    topic = request.form["topic"]
    check_topic = db.session.execute(text("SELECT Topic FROM conversations WHERE Topic=:topic"), {"topic":topic}).fetchone()
    if not check_topic:
        session["error"]="topic_not_found_error"
        return redirect("/error")
    sql_conversations = "DELETE FROM conversations WHERE Topic=:topic"
    db.session.execute(text(sql_conversations), {"topic":topic})
    sql_remove = "DROP TABLE " + topic
    db.session.execute(text(sql_remove))
    db.session.commit()
    return redirect("/")


@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/return_from_error")
def return_from_error():
    del session["error"]
    return redirect("/")
