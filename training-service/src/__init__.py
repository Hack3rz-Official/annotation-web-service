from flask import Blueprint
from flask_restx import Api
from .controllers.training import api as training

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(
    blueprint,
    version="1.0",
    title="Training Service API",
)
api.add_namespace(training)