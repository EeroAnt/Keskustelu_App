from app import app
from src.login import _logout, _register, _login
from src.topics import _create, _remove
from src.edit import _edit_message, _edit_header
from src.delete import _remove_message, _remove_conversation
from src.navigation import _index, _go_to_topic, _go_to_conversation, _go_to_edit_message, _go_to_edit_header
from src.messaging import _send_message, _start_conversation
from src.search import _search
from src.clearance import _give_clearance

@app.route("/")
def index():
    return _index()


@app.route("/topic<int:topic_id>")
def go_to_topic(topic_id):
    return _go_to_topic(topic_id)


@app.route("/topic<int:topic_id>/start", methods=["POST","GET"])
def start_conversation(topic_id):
    return _start_conversation(topic_id)


@app.route("/topic<int:topic_id>/conversation<int:header_id>")
def go_to_conversation(topic_id, header_id):
    return _go_to_conversation(topic_id, header_id)


@app.route("/remove_conversation", methods=["POST","GET"])
def remove_conversation():
    return _remove_conversation()


@app.route("/go_to_edit_header", methods=["POST","GET"])
def go_to_edit_header():
    return _go_to_edit_header()


@app.route("/edit_header", methods=["POST","GET"])
def edit_header():
    return _edit_header()


@app.route("/topic<int:topic_id>/conversation<int:header_id>", methods=["POST","GET"])
def send_message(topic_id, header_id):
    return _send_message(topic_id, header_id)


@app.route("/remove_message", methods=["POST","GET"])
def remove_message():
    return _remove_message()


@app.route("/go_to_edit_message", methods=["POST","GET"])
def go_to_edit_message():
    return _go_to_edit_message()


@app.route("/edit_message", methods=["POST","GET"])
def edit_message():
    return _edit_message()


@app.route("/login",methods=["POST"])
def login():
    return _login()


@app.route("/logout")
def logout():
    return _logout()


@app.route("/register", methods=["POST","GET"])
def register():
    return _register()


@app.route("/create", methods=["POST","GET"])
def create():
    return _create()


@app.route("/remove", methods=["POST","GET"])
def remove():
    return _remove()

@app.route("/search", methods=["POST","GET"])
def search():
    return _search()

@app.route("/give_clearance", methods=["POST","GET"])
def give_clearance():
    return _give_clearance()