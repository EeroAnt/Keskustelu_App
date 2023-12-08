from src.db import db
from sqlalchemy import text
from src.time_formatter import format_timestamp
from flask import session
from src.user_status import is_admin


def _listing_for_index():
    return _topics_with_headers() + _topics_without_headers()


def _check_clearances():
	if is_admin():
		return "SELECT * FROM topics"
	else:
		try:
			user = session["username"]
			sql1 = f"SELECT level FROM clearances WHERE username='{user}'"
			sql2 = f"SELECT * FROM topics, ({sql1}) AS user_clearance WHERE topics.secrecy=user_clearance.level OR topics.secrecy IS NULL"
			if db.session.execute(text(sql2)).fetchall() == []:
				return "SELECT * FROM topics WHERE Secrecy IS NULL"
			else:
				return sql2
		except:
			return "SELECT * FROM topics WHERE Secrecy IS NULL"


def _topics_with_headers():
	clearance_check = _check_clearances()
	first_sql = f"SELECT topics.id, topics.topic, count(headers) as headers FROM ({clearance_check}) AS topics, headers WHERE topics.topic=headers.topic GROUP BY topics.id, topics.topic"
	second_sql = "SELECT topics.topic, count(messages) as messages FROM topics, messages WHERE topics.topic=messages.topic GROUP BY topics.topic"
	third_sql = "SELECT topics.topic, MAX(messages.time) as latest FROM topics, messages WHERE topics.topic=messages.topic GROUP BY topics.topic"
	sql = f"SELECT First.id, First.topic, headers, messages, latest FROM ({first_sql}) AS First LEFT JOIN ({second_sql}) AS Second ON First.topic=Second.topic LEFT JOIN ({third_sql}) as Third ON First.topic=Third.topic"
	temp_topics = db.session.execute(text(sql)).fetchall()
	topics = []
	for topic in temp_topics:
		if topic.latest:
			topics.append(dict(id=topic.id,topic=topic.topic, headers=topic.headers, messages=topic.messages, latest=format_timestamp(topic.latest)))
		else:
			topics.append(dict(id=topic.id,topic=topic.topic, headers=topic.headers, messages=0, latest=""))
	return topics


def _topics_without_headers():
	topics = []
	clearance_check = _check_clearances()
	sql = f"SELECT DISTINCT topics.id, topics.topic from ({clearance_check}) AS topics WHERE topics.topic not in (SELECT DISTINCT headers.topic FROM headers);"
	temp_topics = db.session.execute(text(sql)).fetchall()
	for topic in temp_topics:
		topics.append(dict(id=topic.id,topic=topic.topic, headers=0, messages=0, latest=""))
	return topics


def get_topics_headers_and_ids(input):
	clearance_check = _check_clearances()
	first_sql = f"SELECT topic, header FROM messages WHERE message LIKE '%{input}%' GROUP BY topic, header"
	checked_sql = f"SELECT unchecked.topic, unchecked.header FROM ({first_sql}) AS unchecked, ({clearance_check}) AS topics WHERE unchecked.topic=topics.topic"
	second_sql = f"SELECT topics_and_headers.topic, topics_and_headers.header, topics.id FROM topics LEFT JOIN ({checked_sql}) AS topics_and_headers ON topics_and_headers.topic=topics.topic"
	sql = f"SELECT topic_id_added.topic, topic_id_added.header, topic_id_added.id AS topic_id, headers.id as header_id FROM headers LEFT JOIN ({second_sql}) AS topic_id_added ON topic_id_added.header=headers.header;"
	return db.session.execute(text(sql)).fetchall()