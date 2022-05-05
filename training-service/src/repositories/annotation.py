from src.models.annotation import Annotation
import datetime

class AnnotationRepository:

    @staticmethod
    def find_data_to_train_with(lang_name):
        """Fetches data to train with from db for a specific language which has not been used for training so far.

        Args:
            String lang_name
        
        Returns:
            List of objects of class Annotation
        """
        return Annotation.objects(__raw__={"_id.language": lang_name.upper()}, trainedTime__exists=False, validatedTime__exists=False)

    @staticmethod
    def find_validation_data(lang_name):
        """Fetches all (previous) validation data from db for a specific language.

        Args:
            String lang_name
        
        Returns:
            A list of objects of class Annotation
        """
        return Annotation.objects(__raw__={"_id.language": lang_name.upper()}, validatedTime__exists=True)

    @staticmethod
    def update_trained_time(annotations):
        """Updates the field trainedTime on an object of class Annotation with the current timestamp.

        Args:
            An array of annotation objects

        Returns:
            None, updates the field trainedTime on the used training data on the db such that it won´t be used
            for future training processes and thus prevent a potential overfit.
        """
        annotations.update(trainedTime=datetime.datetime.now())

    @staticmethod
    def update_validated_time(annotations):
        """Updates the field validatedTime on an object of class Annotation with the current timestamp.

        Args:
            An array of annotation objects

        Returns:
            None, updates the field validatedTime on the used validation data on the db such that it can be 
            fetched and used for validating a future model.
        """
        annotations.update(validatedTime=datetime.datetime.now())
