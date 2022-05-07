import os
from flask import Flask
from flask_mongoengine import MongoEngine
from apscheduler.schedulers.background import BackgroundScheduler

import config as config
from src.services.training import train_models
from src import blueprint as api_v1

def training_service():
    print("Training Service is alive!", flush=True)
    train_models()

sched = BackgroundScheduler(daemon=True)
sched.add_job(training_service, 'interval', minutes=5)
sched.start()

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
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=os.environ.get('TRAINING_SERVICE_PORT', 5000))
