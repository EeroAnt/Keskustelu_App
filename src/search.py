from flask import render_template, request
from src.db import db
from src.querys import get_topics_headers_and_ids
from src.error import error
from src.time_formatter import format_timestamp
from sqlalchemy import text

def search_func():
	search_input = request.form["search_input"]
	topics_and_headers = get_topics_headers_and_ids(search_input)
	if topics_and_headers == []:
		return error("Hakusanalla ei löytynyt tuloksia")
	messages = _get_messages(search_input)
	return render_template("search_results.html", results = topics_and_headers, messages = messages)


def _get_messages(search_input):
	sql = "SELECT * FROM messages WHERE message LIKE :search_input"
	search_input = "%" + search_input + "%"
	temp_messages = db.session.execute(text(sql), {"search_input":search_input}).fetchall()
	messages = []
	for message in temp_messages:
		messages.append(dict(message=message.message,topic=message.topic,header=message.header,username=message.username,time=format_timestamp(message.time)))
	return messages