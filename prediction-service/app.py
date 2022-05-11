import os
from flask import Flask
from flask_mongoengine import MongoEngine

from src.util.SHModelHelper import init_models
from src import blueprint as api_v1

import logging

def create_app():
    app = Flask(__name__)

    logging.basicConfig()
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.DEBUG)

    # Connect to database
    app.config["MONGODB_SETTINGS"] = {
        'db': os.environ.get('MONGO_DATABASE_NAME'),
        'host': os.environ.get('MONGO_HOST', "test"),
        'port': int(os.environ.get('MONGO_PORT', 0)),
        'username': os.environ.get('MONGO_USERNAME'),
        'password': os.environ.get('MONGO_PASSWORD'),
        'authSource': os.environ.get('MONGO_AUTH_DATABASE')
    }
    db = MongoEngine()
    db.init_app(app)

    # Register API
    app.register_blueprint(api_v1)

    init_models()

    logger.info("Prediction Service started successfully!")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=os.environ.get('PREDICTION_SERVICE_PORT', 5000))
