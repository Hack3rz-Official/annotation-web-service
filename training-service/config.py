import logging
import os

HOST = "127.0.0.1"
PORT = 8085
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
