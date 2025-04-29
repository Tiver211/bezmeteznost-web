from flask import Blueprint, jsonify, request, flash, redirect
from api.models import *
from api.services.auth import *
from flask_login import login_user, login_required, logout_user
from api.extensions import redis_client

blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@blueprint.route("/register", methods=["POST"], endpoint='register')
def register():
    mail = request.json.get("mail")
    login = request.json.get("login")
    password = request.json.get("password")
    token = request.json.get("token")

    if not validate_captcha(token, request.headers.get("X-Real-IP")):
        return jsonify({"msg": "bad captcha"}), 403

    code = register_user(mail, login, password)
    if not code == 200:
        flash('Error, try again later')
        return jsonify({"msg": "error while creating user"}), code

    return jsonify({"msg": "ok"})

@blueprint.route("/login", methods=["POST"], endpoint='login')
def login():
    mail = request.json.get("mail")
    password = request.json.get("password")
    token = request.json.get("token")

    if not validate_captcha(token, request.headers.get("X-Real-IP")):
        return jsonify({"msg": "bad captcha"}), 403

    code, user = authenticate_user(mail, password)
    if code != 200:
        flash('incorrect login or password')
        return jsonify({"msg": "incorrect login or password"}), code

    login_user(user)

    return jsonify({"msg": "ok"})

@blueprint.route("/verify_mail", methods=["GET"])
def verify_mail():
    token = request.args.get("token")
    status, user = verify_user_mail(token)
    if status != 200:
        return jsonify({"msg": "Error while verify mail"}), status

    login_user(user)
    return redirect("/")

@blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"msg": "ok"}), 200

@blueprint.route("resend", methods=["POST"])
@login_required
def resend_mail():
    generate_mail_verification_request(current_user)
    return jsonify({"msg": "ok"}), 200