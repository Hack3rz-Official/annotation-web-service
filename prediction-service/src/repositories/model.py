from src.models.model import Model
from src.util.SHModelUtils import SHModel
import os

class ModelRepository:

    @staticmethod
    def find_best_model(lang_name):
        return Model.objects(language=lang_name).order_by('-createdTime').first()
