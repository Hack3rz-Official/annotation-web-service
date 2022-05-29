import os
from src.util.SHModelUtils import SHModel
from src.model.model import Model
import logging
logger = logging.getLogger('waitress')

def get_model_path(lang_name):
    """Gets the path of a model based on its programming language

    Args:
        String which is "python3", "java" or "kotlin"
    
    Returns:
        Path of requested model
    """
    return F"{lang_name.lower()}_{os.environ.get('MODEL_NAME')}.pt"


def from_db_model_to_sh_model(db_model, lang_name):
    """Gets a model file which is in the format of a binary file with the most recent createdTime 
    and converts it into an SHModel such that it can be used for trainng purposes.

    Args:
        db_model (binary file) and string lang_name

    Returns:
        SHModel of a specific language
    """
    if db_model:
        logger.info(f"[SHModel] Newest Model loaded from DB with createdTime {db_model.createdTime}")
        with open(get_model_path(lang_name), "wb") as file:
            model_file = db_model.file.read()
            file.write(model_file)
    else:
        logger.info("[SHModel] No model found in DB, creating new model")

    return SHModel(lang_name.lower(), os.environ.get('MODEL_NAME'))


def from_best_sh_model_to_db_model(lang_name, accuracy, training_data_amount, validation_data_amount):
    """Saves a SHModel from current directory to the db with the language name and the accomplished accurarcy.

    Args:
        String lang_name and an accuracy (integer between [0,1]) 

    Returns:
        An object of class Model which is the representation of an SHModel for the database annotation called models.
    """
    logger.info("[TRAIN] New Model saved from directory to DB ")
    model = Model(language=lang_name.upper(), accuracy=accuracy, trainingDataAmount=training_data_amount, validationDataAmount=validation_data_amount)
    with open(get_model_path(lang_name), "rb") as binary_file:
        model.file.put(binary_file)

    return model
