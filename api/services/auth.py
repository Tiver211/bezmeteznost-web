import json
import os
from datetime import timedelta

from api.extensions import redis_client
from api.models import *
import bcrypt
import requests
from sqlalchemy import or_
import secrets
from api.validators import validate_schema, UserSchema
from api.services.smtp import send_verification_mail

def validate_captcha(token: str, user_ip: str) -> bool:
    answer = requests.post("https://smartcaptcha.yandexcloud.net/validate",
                           data={"secret": os.getenv("CAPTCHA_TOKEN"), "token": token, "ip": user_ip})

    if answer.status_code == 200 or answer.json().get("status") == "ok":
        return True

    return False


def create_user(mail: str, login: str, password_hash: str):
    user = User(mail=mail, login=login, password_hash=password_hash)

    db.session.add(user)
    db.session.commit()
    return user


def register_user(mail, login, password):
    if not validate_schema(UserSchema, mail=mail, login=login, password=password):
        return 400

    if not check_user_unique(mail, login):
        return 409

    password_hash = create_password_hash(password)

    user = create_user(mail, login, password_hash)
    generate_mail_verification_request(user)

    return 200

def create_password_hash(password: str):
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return pw_hash

def check_user_unique(mail, login):
    user = User.query.filter(or_(User.mail == mail, User.login == login)).all()
    if not user:
        return True

    return False

def authenticate_user(mail, password):
    user = User.query.filter_by(mail=mail, verify_mail=True).first()

    if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return 401, None

    if not user.verify_mail:
        return 423, user

    return 200, user

def generate_mail_verification_request(user):
    mail = user.mail
    login = user.login
    user_id = user.id

    token = generate_verification_token()
    redis_client.set(f"verify_mail:{token}", str(user_id), ex=timedelta(days=1))
    send_verification_mail(token, mail, login)


def generate_verification_token():
    return secrets.token_urlsafe()

def verify_user_mail(token):
    user_id = redis_client.get(f"verify_mail:{token}")
    if user_id is None:
        return 404, None

    user = get_user_by_id(user_id)
    user.verify_mail = True
    db.session.commit()

    return 200, user

def get_user_by_id(user_id):
    return User.query.get(user_id)
