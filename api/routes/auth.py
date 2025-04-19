from flask import Blueprint, jsonify, request
from api.models import *
from api.services.auth import *

blueprint = Blueprint("/auth", __name__, url_prefix="auth")

@blueprint.route("/register", methods=["POST"])
def register():
    login = request.json.get("login")
    password = request.json.get("password")

    if User.query.filter_by(login=login).first():
        return jsonify({"msg": "this login already exist"}), 409

    code, user_id = create_user(login, password)
    if not code == 200:
        return jsonify({"msg": "error while creating user"}), code

    return create_jwt_token_user(code)

@blueprint.route("/login", methods=["POST"])
def login():
    login = request.json.get("login")
    password = request.json.get("password")

    code, user_id = login_user(login, password)
    if code != 200:
        return jsonify({"msg": "incorrect login or password"})

    return create_jwt_token_user(user_id)


