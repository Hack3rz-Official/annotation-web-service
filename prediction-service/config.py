import logging
import os

DEBUG = os.getenv("ENVIRONEMENT") == "DEV"
HOST = "127.0.0.1"
PORT = 8084
SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Training Service API",
        "description": "Version 1 of the API",
    }
}
SWAGGER_CONFIG = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'api_spec_v1',
            "route": '/api_spec_v1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/api/docs/"
}
SUPPORTED_LANGUAGES = ["java", "python3", "kotlin"]
MODEL_NAME = "cur"

"""
logging.basicConfig(
    filename=os.getenv("APP_LOG", "app.log"),
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s \
        pid:%(process)s module:%(module)s %(message)s",
    datefmt="%d/%m/%y %H:%M:%S",
)
"""
