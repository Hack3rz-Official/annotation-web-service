from src.models.model import Model
from src.util.SHModelUtils import SHModel
import os

class ModelRepository:

    @staticmethod
    def find_best_model(lang_name):
        """Fetches most recent model (and thus model with highest accuracy) from db.

        Args:
            String lang_name. 
        
        Returns:
            Returns a model for a specific language from db. 
        """
        return Model.objects(language=lang_name).order_by('-createdTime').first()

    @staticmethod
    def save(model):
        #Saves model to db.
        model.save()
