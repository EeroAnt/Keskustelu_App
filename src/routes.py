from app import app
from src.login import logout_func, register_func, login_func
from src.topics import create_func, remove_func
from src.edit import edit_message_func, edit_header_func
from src.delete import remove_message_func, remove_conversation_func
from src.navigation import to_index, to_topic, to_conversation, to_edit_message, to_edit_header
from src.messaging import send_message_func, start_conversation_func
from src.search import search_func
from src.clearance import give_clearance_func

@app.route("/")
def index():
	return to_index()


@app.route("/topic<int:topic_id>")
def go_to_topic(topic_id):
	return to_topic(topic_id)


@app.route("/topic<int:topic_id>/start", methods=["POST","GET"])
def start_conversation(topic_id):
	return start_conversation_func(topic_id)


@app.route("/topic<int:topic_id>/conversation<int:header_id>")
def go_to_conversation(topic_id, header_id):
	return to_conversation(topic_id, header_id)


@app.route("/remove_conversation", methods=["POST","GET"])
def remove_conversation():
	return remove_conversation_func()


@app.route("/go_to_edit_header", methods=["POST","GET"])
def go_to_edit_header():
	return to_edit_header()


@app.route("/edit_header", methods=["POST","GET"])
def edit_header():
	return edit_header_func()


@app.route("/topic<int:topic_id>/conversation<int:header_id>", methods=["POST","GET"])
def send_message(topic_id, header_id):
	return send_message_func(topic_id, header_id)


@app.route("/remove_message", methods=["POST","GET"])
def remove_message():
	return remove_message_func()


@app.route("/go_to_edit_message", methods=["POST","GET"])
def go_to_edit_message():
	return to_edit_message()


@app.route("/edit_message", methods=["POST","GET"])
def edit_message():
	return edit_message_func()


@app.route("/login",methods=["POST"])
def login():
	return login_func()


@app.route("/logout")
def logout():
	return logout_func()


@app.route("/register", methods=["POST","GET"])
def register():
	return register_func()


@app.route("/create", methods=["POST","GET"])
def create():
	return create_func()


@app.route("/remove", methods=["POST","GET"])
def remove():
	return remove_func()

@app.route("/search", methods=["POST","GET"])
def search():
	return search_func()

@app.route("/give_clearance", methods=["POST","GET"])
def give_clearance():
	return give_clearance_func()