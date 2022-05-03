from src.models.annotation import Annotation
import datetime

class AnnotationRepository:

    @staticmethod
    def find_training_data(lang_name):
        """Fetches training data from db for a specific language which has not been used for training so far.

        Args:
            String lang_name
        
        Returns:
            An object of class Annotation
        """
        return Annotation.objects(__raw__={"_id.language": lang_name.upper()}, trainedTime__exists=False)

    @staticmethod
    def update_trained_time(annotations):
        """Updates the field trainedTime on an object of class Annotation

        Args:
            An arrays of annotation objects

        Returns:
            None, updates the field trainedTime on the used training data on the db such that it won´t be used
            for future training processes and thus prevent a potential overfit.
            
        """
        annotations.update(trainedTime=datetime.datetime.now())
