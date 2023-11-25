from flask import Flask
from os import getenv
from src.db import db
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URI')
db.init_app(app)
import src.routes