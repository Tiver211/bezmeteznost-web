from flask import Blueprint

from api.routes.api import blueprint as api

blueprint = Blueprint("main", __name__)

blueprint.register_blueprint(api)