from functools import wraps
from api.services.auth import verify_required
from flask import Blueprint, render_template, request, redirect, url_for, send_file, send_from_directory, current_app
from flask_login import login_required, current_user

blueprint = Blueprint("pages", __name__)


@blueprint.route("/login", methods=["GET"], endpoint='login_page')
def login():
    return render_template("login.html")

@blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@blueprint.route("/register", methods=["GET"], endpoint='register_page')
def register():
    return render_template("register.html")

@blueprint.route("/settings", methods=["GET"])
@login_required
@verify_required
def settings():
    return render_template("settings.html", user_ip=request.headers.get("X-Real-IP"), username=current_user.login)
  
@blueprint.route("/verify_page", methods=["GET"])
@login_required
def verify_page():
    if getattr(current_user, 'verify_mail', False):
        return redirect('/')

    return render_template('verify_page.html', mail=current_user.mail), 200

@blueprint.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory(
        current_app.static_folder,  # Путь к папке static
        'favicon.ico',  # Имя файла
        mimetype='image/vnd.microsoft.icon'  # MIME-тип для .ico
    )

