from flask import Blueprint
from api.routes.auth import blueprint as auth_blueprint

blueprint = Blueprint("main", __name__, url_prefix="/api")
blueprint.register_blueprint(auth_blueprint)