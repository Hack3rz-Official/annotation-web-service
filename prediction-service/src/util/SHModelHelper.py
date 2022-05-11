import os
from src.repository.model import ModelRepository
from functools import wraps
from time import process_time
import logging
logger = logging.getLogger('waitress')

def measure(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(process_time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(process_time() * 1000)) - start
            logger.debug(
                f"Total execution time {func.__name__}: {end_ if end_ > 0 else 0} ms"
            )

    return _time_it


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
    if db_model:
        logger.debug(f"[SHModel] Newest Model loaded from DB with createdTime {db_model.createdTime}")
        with open(get_model_path(lang_name), "wb") as file:
            model_file = db_model.file.read()
            file.write(model_file)
    else:
        logger.debug(f"[SHModel] No model found in DB for lang {lang_name}, new model will be created")


@measure
def init_models():
    model_repository = ModelRepository()
    model_repository.check_for_better_model("PYTHON3")
    model_repository.check_for_better_model("KOTLIN")
    model_repository.check_for_better_model("JAVA")
