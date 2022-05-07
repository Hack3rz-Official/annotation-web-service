import os
from flask import Flask
from flask_mongoengine import MongoEngine

from src.repository.model import ModelRepository
from src.util.SHModelHelper import load_db_model_to_current_directory    
from src import blueprint as api_v1

def create_app():
    app = Flask(__name__)

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
    app.run(debug=True, port=os.environ.get('PREDICTION_SERVICE_PORT', 5000))
