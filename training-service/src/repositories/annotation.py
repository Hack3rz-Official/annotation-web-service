from src.models.annotation import Annotation
import datetime

class AnnotationRepository:

    @staticmethod
    def find_training_data(lang_name):
        return Annotation.objects(__raw__={"_id.language": lang_name.upper()}, trainedTime__exists=False)

    @staticmethod
    def update_trained_time(annotations):
        annotations.update(trainedTime=datetime.datetime.now().astimezone())
