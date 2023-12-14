from flask import render_template, abort, redirect, request, session
from src.querys import listing_for_index, get_headers_for_topic, get_messages, get_message, get_header, get_topic, get_message_owner
from src.clearance import check_clearance_level


def to_index():
	return render_template("index.html", topics=listing_for_index())


def to_topic(topic_id):
	if check_clearance_level(topic_id):
		result = get_headers_for_topic(topic_id)
		topic = get_topic(topic_id)
		return render_template("topic.html", conversations=result, topic_id=topic_id, topic=topic)
	else:
		abort(404)


def to_conversation(topic_id, header_id):
	if check_clearance_level(topic_id):
		messages, topic, header = get_messages(topic_id, header_id)
		return render_template("conversation.html", messages=messages, topic_id=topic_id, header_id=header_id, topic=topic, header=header)
	else:
		abort(404)


def to_edit_message():
	session["edit"] = "message"
	message = get_message(request.form["message_id"])
	message_owner = get_message_owner(request.form["message_id"])
	header= get_header(request.form["header_id"])
	topic = get_topic(request.form["topic_id"])
	return render_template("edit.html",
						message=message,
						message_owner=message_owner,
						message_id=request.form["message_id"],
						topic_id=request.form["topic_id"],
						topic=topic, 
						header_id=request.form["header_id"],
						header = header)


def to_edit_header():
	session["edit"] = "header"
	header = get_header(request.form["header_id"])
	return render_template("edit.html", header=header, header_id=request.form["header_id"], topic_id=request.form["topic_id"], topic=request.form["topic"])


def return_from_edit(topic_id="", header_id=""):
	if session["edit"] == "message":
		del session["edit"]
		return redirect(f"/topic{topic_id}/conversation{header_id}")
	elif session["edit"] == "header":
		del session["edit"]
		return redirect(f"/topic{topic_id}")