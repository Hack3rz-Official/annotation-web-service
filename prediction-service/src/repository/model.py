from src.model.model import Model
from src.repository import store
import logging
logger = logging.getLogger('waitress')

class ModelRepository:
    """
    The repository handling the storing and retrieving of models from the internal (i.e in-memory)
    store or the database.
    """

    def set_model(self, lang_name, new_model):
        store.models[lang_name] = new_model

    def get_models(self):
        return store.models

    def get_model(self, lang_name):
        return store.models[lang_name]

    def reset(self):
        """
        Resets the internal store (mostly used for testing / debugging purposes)
        """
        store.models = {
            'PYTHON3': None,
            'JAVA': None,
            'KOTLIN': None
        }
        logger.debug("[ModelRepository] models have been reset")

    def check_for_better_model(self, lang_name):
        """
        Checks the external db for a better model and updates the internal store
        :param lang_name: the name of the language
        :return: Model: the best model
        """
        best_model = self.find_best_model(lang_name)
        current_model = store.models[lang_name]

        if current_model is None or best_model.accuracy <= current_model.accuracy:
            return best_model

        self.set_model(lang_name, best_model)
        return best_model

    def get_or_fetch_model(self, lang_name):
        """
        Gets the model from the internal store or fetches it from the db if it doesn't exist
        :param lang_name: the language
        :return: Model: the model
        """
        current_model = store.models[lang_name]
        if current_model is None:
            current_model = self.find_best_model(lang_name)
            self.set_model(lang_name, current_model)
        return current_model

    @staticmethod
    def find_best_model(lang_name):
        """
        Finds the best model in the database
        :param lang_name: the language
        :return: Model: the model
        """
        return Model.objects(language=lang_name).order_by('-createdTime').first()
