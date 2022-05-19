from src.model.model import Model

class ModelRepository:

    @staticmethod
    def find_best_model(lang_name):
        """Fetches most recent model (and thus model with highest accuracy) from db.

        Args:
            String lang_name. 
        
        Returns:
            Returns a model for a specific language from db. 
        """
        return Model.objects(language=lang_name.upper()).order_by('-createdTime').first()

    @staticmethod
    def save(model):
        # Saves model to db.
        model.save()
