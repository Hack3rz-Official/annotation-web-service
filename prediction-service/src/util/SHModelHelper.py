import os
from src.repository.model import ModelRepository
from src.util.measure import measure
import logging
logger = logging.getLogger('waitress')


def get_model_path(lang_name):
    """
    Creates the path of the model based on the language name and the
    model name specified in the MODEL_NAME environment variable
    :param lang_name: string with the language of the model
    :return: String the path for the model
    """
    return F"{lang_name.lower()}_{os.environ.get('MODEL_NAME')}.pt"


@measure
def load_db_model_to_current_directory(db_model, lang_name):
    """
    Loads the model from the database and saves it in the current directory
    :param db_model: the model from the db
    :param lang_name: the name of the language (used in the file name)
    """
    if db_model:
        logger.debug(f"[SHModel] Newest Model loaded from DB with createdTime {db_model.createdTime}")
        with open(get_model_path(lang_name), "wb") as file:
            model_file = db_model.file.read()
            file.write(model_file)
    else:
        logger.debug(f"[SHModel] No model found in DB for lang {lang_name}, new model will be created")


