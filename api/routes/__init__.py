from flask import Blueprint
from .pages import blueprint as pages
from api.routes.api import blueprint as api

blueprint = Blueprint("main", __name__)

blueprint.register_blueprint(api)
blueprint.register_blueprint(pages)