from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

blueprint = Blueprint("pages", __name__)


@blueprint.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@jwt_required()
@blueprint.route("/", methods=["GET"])
def login():
    return render_template("index.html")

@blueprint.route("/register", methods=["GET"])
def login():
    return render_template("register.html")
