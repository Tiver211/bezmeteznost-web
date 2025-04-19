from flask_jwt_extended import create_access_token
from api.extensions import jwt, db
from api.models import *
import bcrypt

def create_user(login, password):
    pwhash = get_hash(password)

    user = User(login=login, password_hash=pwhash)

    db.session.ad(user)
    db.session.commit()

    user_id = user.id
    return 200, user_id

def get_hash(password):
    pwhash = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt(rounds=5))

    return pwhash.decode()

def create_jwt_token_user(user_id):
    access_token = create_access_token(identity=user_id,
                                       additional_claims={"id": user_id})

    return access_token

def login_user(login, password):
    user = User.query.filter_by(login=login).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return 401, None, None, None

    return 200, user.id