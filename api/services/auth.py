import os

from api.models import *
import bcrypt
import requests

def create_user(login, password):
    pwhash = get_hash(password)

    user = User(login=login, password_hash=pwhash)

    db.session.add(user)
    db.session.commit()

    user_id = user.id
    return 200, user_id

def get_hash(password):
    pwhash = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt(rounds=5))

    return pwhash.decode()

def login_user_func(login, password):
    user = User.query.filter_by(login=login).first()
    print(user, flush=True)
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return 401, None

    return 200, user.id

def get_user_by_id(user_id):
    user = User.query.get(user_id)
    return user

def validate_capcha(token, user_ip):
    answer = requests.post("https://smartcaptcha.yandexcloud.net/validate", data={"secret": os.getenv("CAPTCHA_TOKEN"), "token": token, "ip": user_ip})
    if not answer.status_code == 200 or not answer.json().get("status") == "ok":
        return False

    return True