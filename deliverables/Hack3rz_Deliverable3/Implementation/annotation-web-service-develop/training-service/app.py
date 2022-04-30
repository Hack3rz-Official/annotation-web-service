from flask import Flask
from flask_mongoengine import MongoEngine
from apscheduler.schedulers.background import BackgroundScheduler
from flasgger import Swagger
import os
import config as config
from src.blueprints.training import training_blueprint
from src.services.training import train_models

def training_service():
    print("Training Service is alive!", flush=True)
    train_models()

sched = BackgroundScheduler(daemon=True)
sched.add_job(training_service, 'interval', minutes=5)
sched.start()

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
    app.register_blueprint(training_blueprint, url_prefix="/api/v1/training")

    # Init Swagger
    Swagger(app, config=config.SWAGGER_CONFIG, template=config.SWAGGER_TEMPLATE)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host=config.HOST, port=config.PORT)
