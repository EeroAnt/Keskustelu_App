from flask import render_template, request
from src.db import db
from src.error import error
from src.time_formatter import format_timestamp
from sqlalchemy import text

def _search():
    search_input = request.form["search_input"]
    topics_and_headers = _get_topics_and_headers(search_input)
    if topics_and_headers == []:
        return error("no_search_results")
    topics_and_headers_with_urls = _get_urls(topics_and_headers)
    messages = _get_messages(search_input)
    return render_template("search_results.html", results = topics_and_headers_with_urls, messages = messages)

def _get_topics_and_headers(search_input):
    search_input = "%" + search_input + "%"
    sql = "SELECT topic, header FROM messages WHERE message LIKE :search_input GROUP BY topic, header"
    temp_topics_and_headers = db.session.execute(text(sql), {"search_input":search_input}).fetchall()
    topics_and_headers = []
    for topic_and_header in temp_topics_and_headers:
        topics_and_headers.append(dict(topic=topic_and_header.topic,header=topic_and_header.header))
    return topics_and_headers

def _get_urls(topics_and_headers):
    for topic_and_header in topics_and_headers:
        topic = topic_and_header["topic"]
        header = topic_and_header["header"]
        sql = "SELECT id FROM topics WHERE topic = :topic"
        topic_id = db.session.execute(text(sql), {"topic":topic}).fetchone()[0]
        sql = "SELECT id FROM headers WHERE header = :header AND topic = :topic"
        header_id = db.session.execute(text(sql), {"header":header, "topic":topic}).fetchone()[0]
        topic_and_header["url"] = "/topic" + str(topic_id) + "/conversation" + str(header_id)
    return topics_and_headers

def _get_messages(search_input):
    sql = "SELECT * FROM messages WHERE message LIKE :search_input"
    temp_messages = db.session.execute(text(sql), {"search_input":search_input}).fetchall()
    messages = []
    for message in temp_messages:
        messages.append(dict(message=message.message,topic=message.topic,header=message.header,username=message.username,time=format_timestamp(message.time)))
    return messages