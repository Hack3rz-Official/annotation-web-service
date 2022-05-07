from flask import Blueprint
from flask_restx import Api
from .controller.prediction import api as prediction

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(
    blueprint,
    version="1.0",
    title="Prediction Service API",
)
api.add_namespace(prediction)
