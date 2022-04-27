import os
import config as config
from flask import Flask
from flask_mongoengine import MongoEngine
from flasgger import Swagger

from src.blueprints.prediction import prediction_blueprint
from src.repositories.model import ModelRepository
from src.util.SHModelHelper import load_db_model_to_current_directory

def create_app():
    app = Flask(__name__)
    app.debug = config.DEBUG
    app.config["MONGODB_SETTINGS"] = {
        'db': os.environ.get('MONGO_DATABASE_NAME'),
        'host': os.environ.get('MONGO_HOST'),
        'port': int(os.environ.get('MONGO_PORT')),
        'username': os.environ.get('MONGO_USERNAME'),
        'password': os.environ.get('MONGO_PASSWORD'),
        'authSource': os.environ.get('MONGO_AUTH_DATABASE')
    }  

    # Connect to database
    db = MongoEngine()
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(prediction_blueprint, url_prefix="/api/v1/prediction")

    # Init Swagger  
    Swagger(app, config=config.SWAGGER_CONFIG, template=config.SWAGGER_TEMPLATE)

    # returns binary file of newest model from db for python3, kotlin, java
    db_model_python = ModelRepository.find_best_model("PYTHON3")
    db_model_kotlin = ModelRepository.find_best_model("KOTLIN")
    db_model_java = ModelRepository.find_best_model("JAVA")

    # safes current model of each language to root directory
    load_db_model_to_current_directory(db_model_python, "PYTHON3")
    load_db_model_to_current_directory(db_model_kotlin, "KOTLIN")
    load_db_model_to_current_directory(db_model_java, "JAVA")

    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
