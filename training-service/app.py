import os
from flask import Flask
from mongoengine import connect
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from src.service.training import train_models
from src import blueprint as api_v1

import logging
logging.basicConfig()
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)
    
def training_service():
    """
    Function that is used to schedule the training
    """
    logger.info("Training Service is alive!")
    train_models()

sched = BackgroundScheduler(daemon=True)
sched.add_job(training_service, 'interval', minutes=5)
sched.start()

def create_app():
    """
    Main function for initializing the flask app
    :return: the flask app
    """
    app = Flask(__name__)

    # allow swagger-ui
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:" + os.environ.get('SWAGGER_UI_PORT', "0"), "send_wildcard": "False"}})

    # Connect to database
    connect(host=os.environ.get('DB_CONNECTION_STRING'))

    # Register API
    app.register_blueprint(api_v1)
        
    logger.info("Training Service started successfully!")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=os.environ.get('TRAINING_SERVICE_PORT', 5000))
