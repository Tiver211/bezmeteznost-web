from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

blueprint = Blueprint("pages", __name__)


@blueprint.route("/login", methods=["GET"], endpoint='login_page')
def login():
    return render_template("login.html")

@blueprint.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html", username=current_user.login, user_ip=request.remote_addr)

@blueprint.route("/register", methods=["GET"], endpoint='register_page')
def register():
    return render_template("register.html")

@blueprint.route("/settings", methods=["GET"])
def settings():
    return render_template("settings.html")