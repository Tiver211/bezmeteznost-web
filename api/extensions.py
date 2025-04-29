import os

import flask_login
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import flask_mail
import redis

db = SQLAlchemy()

login_manager = flask_login.LoginManager()

mail = flask_mail.Mail()

redis_client = redis.Redis(
    host=os.getenv("REDIS_CONN").split(':')[0],
    port=os.getenv("REDIS_CONN").split(':')[1],
    decode_responses=True)