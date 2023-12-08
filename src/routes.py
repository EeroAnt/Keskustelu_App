from app import app
from src.login import logout, register, login
from src.topics import create, remove
from src.edit import edit_message, edit_header
from src.delete import remove_message, remove_conversation
from src.navigation import index, to_topic, to_conversation, to_edit_message, to_edit_header
from src.messaging import send_message, start_conversation
from src.search import search
from src.clearance import give_clearance

@app.route("/")
def index():
	return index()


@app.route("/topic<int:topic_id>")
def go_to_topic(topic_id):
	return to_topic(topic_id)


@app.route("/topic<int:topic_id>/start", methods=["POST","GET"])
def start_conversation(topic_id):
	return start_conversation(topic_id)


@app.route("/topic<int:topic_id>/conversation<int:header_id>")
def go_to_conversation(topic_id, header_id):
	return to_conversation(topic_id, header_id)


@app.route("/remove_conversation", methods=["POST","GET"])
def remove_conversation():
	return remove_conversation()


@app.route("/go_to_edit_header", methods=["POST","GET"])
def go_to_edit_header():
	return to_edit_header()


@app.route("/edit_header", methods=["POST","GET"])
def edit_header():
	return edit_header()


@app.route("/topic<int:topic_id>/conversation<int:header_id>", methods=["POST","GET"])
def send_message(topic_id, header_id):
	return send_message(topic_id, header_id)


@app.route("/remove_message", methods=["POST","GET"])
def remove_message():
	return remove_message()


@app.route("/go_to_edit_message", methods=["POST","GET"])
def go_to_edit_message():
	return to_edit_message()


@app.route("/edit_message", methods=["POST","GET"])
def edit_message():
	return edit_message()


@app.route("/login",methods=["POST"])
def login():
	return login()


@app.route("/logout")
def logout():
	return logout()


@app.route("/register", methods=["POST","GET"])
def register():
	return register()


@app.route("/create", methods=["POST","GET"])
def create():
	return create()


@app.route("/remove", methods=["POST","GET"])
def remove():
	return remove()

@app.route("/search", methods=["POST","GET"])
def search():
	return search()

@app.route("/give_clearance", methods=["POST","GET"])
def give_clearance():
	return give_clearance()