from flask import Blueprint
from .auth import blueprint as auth_blueprint
from .ips import blueprint as ip_blueprint

blueprint = Blueprint("api", __name__, url_prefix="/api")
blueprint.register_blueprint(auth_blueprint)
blueprint.register_blueprint(ip_blueprint)