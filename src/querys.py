from src.db import db
from sqlalchemy import text
from src.time_formatter import format_timestamp

def _listing_for_index():
    first_sql = "SELECT topics.id, topics.topic, count(headers) as headers FROM topics, headers WHERE topics.topic=headers.topic GROUP BY topics.id, topics.topic"
    second_sql = "SELECT topics.topic, count(messages) as messages FROM topics, messages WHERE topics.topic=messages.topic GROUP BY topics.topic"
    third_sql = "SELECT topics.topic, MAX(messages.time) as latest FROM topics, messages WHERE topics.topic=messages.topic GROUP BY topics.topic"
    sql = f"SELECT First.id, First.topic, headers, messages, latest FROM ({first_sql}) AS First LEFT JOIN ({second_sql}) as Second ON First.topic=Second.topic LEFT JOIN ({third_sql}) as Third ON First.topic=Third.topic"
    temp_topics = db.session.execute(text(sql)).fetchall()
    topics = []
    for topic in temp_topics:
        topics.append(dict(id=topic.id,topic=topic.topic, headers=topic.headers, messages=topic.messages, latest=format_timestamp(topic.latest)))
    return topics
