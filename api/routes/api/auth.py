from flask import Blueprint, jsonify, request, flash
from api.models import *
from api.services.auth import *
from flask_login import login_user, login_required, logout_user

blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@blueprint.route("/register", methods=["POST"], endpoint='register')
def register():
    login = request.json.get("username")
    password = request.json.get("password")
    token = request.json.get("token")

    if not validate_capcha(token, request.headers.get("X-Real-IP")):
        return jsonify({"msg": "bad capcha"}), 403

    if User.query.filter_by(login=login).first():
        flash('Username already exists')
        return jsonify({"msg": "this login already exist"}), 409

    code, user_id = create_user(login, password)
    if not code == 200:
        flash('Error, try again later')
        return jsonify({"msg": "error while creating user"}), code

    login_user(get_user_by_id(user_id))

    return jsonify({"msg": "ok"})

@blueprint.route("/login", methods=["POST"], endpoint='login')
def login():
    login = request.json.get("username")
    password = request.json.get("password")
    token = request.json.get("token")

    if not validate_capcha(token, request.headers.get("X-Real-IP")):
        return jsonify({"msg": "bad capcha"}), 403

    code, user_id = login_user_func(login, password)
    if code != 200:
        flash('incorrect login or password')
        return jsonify({"msg": "incorrect login or password"}), 401

    login_user(get_user_by_id(user_id))

    return jsonify({"msg": "ok"})

@blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"msg": "ok"})
