import os
from flask import Flask
from src.repository.model import ModelRepository
from src import blueprint as api_v1
from mongoengine import connect

import logging
logging.basicConfig()
logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)


def create_app():
    """
    Handles the initialization of the flask application.
    :return: the flask app
    """
    app = Flask(__name__)

    # Connect to database
    connect(host=os.environ.get('DB_CONNECTION_STRING'))

    # Register API
    app.register_blueprint(api_v1)

    # Load initial models
    model_repository = ModelRepository()
    model_repository.update_models()

    logger.info("Prediction Service started successfully!")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=os.environ.get('PREDICTION_SERVICE_PORT', 8084))
