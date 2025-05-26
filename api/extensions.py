import os
from gevent import monkey
monkey.patch_all()
from flask_migrate import Migrate
import flask_login
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from celery import Celery
import flask_mail
import redis
from flask_apscheduler import APScheduler

db = SQLAlchemy()

login_manager = flask_login.LoginManager()

mail = flask_mail.Mail()

redis_client = redis.Redis(
    host=os.getenv("REDIS_CONN").split(':')[0],
    port=os.getenv("REDIS_CONN").split(':')[1],
    decode_responses=True)

migrate = Migrate(db=db)
socketio = SocketIO(message_queue=f"redis://{os.getenv('REDIS_CONN')}/0",
                    cors_allowed_origins="*",
                    async_mode="gevent",
                    engineio_logger=True,
                    logger=True)

scheduler = APScheduler()
