from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from flask import redirect, render_template, request, session
from app import app
from src.db import db

@app.route("/")
def index():
    sql = "SELECT * FROM topics"
    result = db.session.execute(text(sql))
    topics = result.fetchall()
    return render_template("index.html", topics=topics)


@app.route("/topic<int:topic_id>")
def go_to_topic(topic_id):
    sql = "SELECT topic FROM topics WHERE id=:topic_id"
    result = db.session.execute(text(sql), {"topic_id":topic_id})
    topic = result.fetchone()[0]
    sql = f"SELECT * FROM headers WHERE topic=:topic"
    result = db.session.execute(text(sql), {"topic":topic})
    conversations = result.fetchall()
    return render_template("topic.html", topic=topic, conversations=conversations, topic_id=topic_id)


@app.route("/topic<int:topic_id>/start", methods=["POST","GET"])
def start_conversation(topic_id):
    header = request.form["header"]
    username = session["username"]
    message = request.form["message"]
    topic = request.form["topic"]
    check_header = db.session.execute(text(f"SELECT header FROM headers WHERE header=:header AND topic=:topic"), {"header":header,"topic":topic}).fetchone()
    if check_header:
        session["error"]="header_error"
        return redirect("/error")
    sql = f"INSERT INTO headers (username, header, topic) VALUES (:username, :header, :topic)"
    db.session.execute(text(sql), {"username":username, "header":header, "topic":topic})
    sql = f"INSERT INTO messages (username, message, time, header, topic) VALUES (:username, :message, NOW(), :header, :topic)"
    db.session.execute(text(sql), {"username":username, "message":message, "header":header, "topic":topic})    
    db.session.commit()
    return redirect(f"/topic{topic_id}")


@app.route("/topic<int:topic_id>/conversation<int:header_id>")
def go_to_conversation(topic_id, header_id):
    topic = db.session.execute(text("SELECT topic FROM topics WHERE id=:topic_id"), {"topic_id":topic_id}).fetchone()[0]
    header = db.session.execute(text("SELECT header FROM headers WHERE id=:header_id"), {"header_id":header_id}).fetchone()[0]
    sql = "SELECT * FROM messages WHERE topic=:topic AND header=:header"
    result = db.session.execute(text(sql), {"topic":topic, "header":header})
    messages = result.fetchall()
    return render_template("conversation.html", messages=messages, topic_id=topic_id, header_id=header_id, topic=topic, header=header)


@app.route("/remove_conversation", methods=["POST","GET"])
def remove_conversation():
    header_id = request.form["header_id"]
    current_user = session["username"]
    header_owner = request.form["header_owner"]
    topic_id = request.form["topic_id"]
    header = db.session.execute(text("SELECT header FROM headers WHERE id=:header_id"), {"header_id":header_id}).fetchone()[0]
    topic = db.session.execute(text("SELECT topic FROM topics WHERE id=:topic_id"), {"topic_id":topic_id}).fetchone()[0]
    if header_owner == current_user:
        sql = "DELETE FROM headers WHERE id=:header_id"
        db.session.execute(text(sql), {"header_id":int(header_id)})
        sql = "DELETE FROM messages WHERE header=:header and topic=:topic"
        db.session.execute(text(sql), {"header":header, "topic":topic})
        db.session.commit()
    else:
        session["error"]="session_error"
        return redirect("/error")
    return redirect(f"/topic{topic_id}")


@app.route("/go_to_edit_header", methods=["POST","GET"])
def go_to_edit_header():
    header_id = request.form["header_id"]
    topic_id = request.form["topic_id"]
    session["edit"] = "header"
    sql = "SELECT * FROM headers WHERE id=:header_id"
    header = db.session.execute(text(sql), {"header_id":int(header_id)}).fetchone()
    return render_template("edit.html", header=header, header_id=header_id, topic_id=topic_id)


@app.route("/edit_header", methods=["POST","GET"])
def edit_header():
    new_header = request.form["new_header"]
    old_header = request.form["old_header"]
    header_id = request.form["header_id"]
    header_owner = request.form["header_owner"]
    session["topic_id"] = request.form["topic_id"]
    current_user = session["username"]
    if header_owner == current_user:
        sql = "UPDATE headers SET header=:header WHERE id=:header_id"
        db.session.execute(text(sql), {"header_id":int(header_id), "header":new_header})
        sql = "UPDATE messages SET header=:header WHERE header=:old_header"
        db.session.execute(text(sql), {"header":new_header, "old_header":old_header})
        db.session.commit()
    else:
        del session["topic_id"]
        del session["edit"]
        session["error"]="session_error"
        return redirect("/error")
    return redirect(f"/return_from_edit")


@app.route("/topic<int:topic_id>/conversation<int:header_id>", methods=["POST","GET"])
def send_message(topic_id, header_id):
    message = request.form["message"]
    topic = request.form["topic"]
    username = session["username"]
    header = request.form["header"]
    sql = f"INSERT INTO messages (username, message, time, topic, header) VALUES (:username, :message, NOW(), :topic, :header)"
    db.session.execute(text(sql), {"username":username, "message":message, "topic":topic, "header":header})
    db.session.commit()
    return redirect(f"/topic{topic_id}/conversation{header_id}")


@app.route("/remove_message", methods=["POST","GET"])
def remove_message():
    message_id = request.form["message_id"]
    current_user = session["username"]
    message_owner = request.form["message_owner"]
    topic_id = request.form["topic_id"]
    header_id = request.form["header_id"]
    if message_owner == current_user:
        sql = "DELETE FROM messages WHERE id=:message_id"
        db.session.execute(text(sql), {"message_id":message_id})
        db.session.commit()
    else:
        session["error"]="session_error"
        return redirect("/error")
    return redirect(f"/topic{topic_id}/conversation{header_id}")


@app.route("/go_to_edit_message", methods=["POST","GET"])
def go_to_edit_message():
    message_id = request.form["message_id"]
    topic_id = request.form["topic_id"]
    header_id = request.form["header_id"]
    session["edit"] = "message"
    sql = "SELECT * FROM messages WHERE id=:message_id"
    message = db.session.execute(text(sql), {"message_id":message_id}).fetchone()
    return render_template("edit.html", message=message, message_id=message_id, topic_id=topic_id, header_id=header_id)


@app.route("/edit_message", methods=["POST","GET"])
def edit_message():
    message = request.form["new_message"]
    message_id = request.form["message_id"]
    message_owner = request.form["message_owner"]
    topic_id = request.form["topic_id"]
    header_id = request.form["header_id"]
    session["topic_id"] = topic_id
    session["header_id"] = header_id
    current_user = session["username"]
    if message_owner == current_user:
        sql = "UPDATE messages SET message=:message WHERE id=:message_id"
        db.session.execute(text(sql), {"message_id":message_id, "message":message})
        db.session.commit()
    else:
        del session["topic_id"]
        del session["header_id"]
        del session["edit"]
        session["error"]="session_error"
        return redirect("/error")
    return redirect(f"/return_from_edit")


@app.route("/return_from_edit", methods=["POST","GET"])
def return_from_edit_message():
    if session["edit"] == "message":
        del session["edit"]
        topic_id = session["topic_id"]
        header_id = session["header_id"]
        del session["topic_id"]
        del session["header_id"]
        return redirect(f"/topic{topic_id}/conversation{header_id}")
    elif session["edit"] == "header":
        del session["edit"]
        topic_id = session["topic_id"]
        del session["topic_id"]
        return redirect(f"/topic{topic_id}")


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
    admin = request.form["admin"]
    hash_value = generate_password_hash(password)
    check_username = db.session.execute(text("SELECT username FROM users WHERE username=:username"), {"username":username}).fetchone()
    if check_username:
        session["error"]="register_error"
        return redirect("/error")
    if admin == '1':
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password , true)"
    else:
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password , false)"
    db.session.execute(text(sql), {"username":username, "password":hash_value})
    db.session.commit()
    return redirect("/")


@app.route("/create", methods=["POST","GET"])
def create():
    topic = request.form["topic"]
    check_topic = db.session.execute(text("SELECT Topic FROM topics WHERE Topic=:topic"), {"topic":topic}).fetchone()
    if check_topic:
        session["error"]="topic_error"
        return redirect("/error")
    sql_topics = "INSERT INTO topics (Topic) VALUES (:topic)"
    db.session.execute(text(sql_topics), {"topic":topic})
    db.session.commit()
    return redirect("/")


@app.route("/remove", methods=["POST","GET"])
def remove():
    topic = request.form["topic"]
    check_topic = db.session.execute(text("SELECT Topic FROM topics WHERE Topic=:topic"), {"topic":topic}).fetchone()
    if not check_topic:
        session["error"]="topic_not_found_error"
        return redirect("/error")
    sql_topics = "DELETE FROM topics WHERE Topic=:topic"
    db.session.execute(text(sql_topics), {"topic":topic})
    sql_headers = "DELETE FROM headers WHERE topic=:topic"
    db.session.execute(text(sql_headers), {"topic":topic})
    sql_messages = "DELETE FROM messages WHERE topic=:topic"
    db.session.execute(text(sql_messages), {"topic":topic})
    db.session.commit()
    return redirect("/")


@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/return_from_error")
def return_from_error():
    del session["error"]
    return redirect("/")
