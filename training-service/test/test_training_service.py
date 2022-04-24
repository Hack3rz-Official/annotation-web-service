import json
from unittest.mock import patch
from hack3rz_test import Hack3rzTest
from src.models.annotation import Annotation, AnnotationKey
from src.services.training import improve_model
import datetime

# run with: python3 -m unittest tests.py
class TrainingServiceTest(Hack3rzTest):

    def test_data_preprocessing(self):
        pass

    def test_split_data(self):
        pass

    def test_accuracy(self):
        pass

    def test_shuffle_data(self):
        pass

    def test_train(self):
        pass
    
    """
    @patch('src.services.training.compute_accuracy')
    @patch('src.services.training.train')
    def test_improve_model_do_nothing(self, train_mock, compute_accuracy_mock):
        train_mock.return_value = []
        compute_accuracy_mock.side_effect = [5, 10]

        improve_model(X, T, "java")
    """
    

    def test_annotation(self):
        annotation = Annotation()
        annotation.key = AnnotationKey(language="JAVA", lexingTokens=[1, 2, 3])
        annotation.sourceCode = "public class HelloWorld { public static void main(String[] args) { System.out.println(\"Hello World\"); } }"
        annotation.highlightingTokens = [1, 2, 3]
        annotation.highlightingCode = "public class HelloWorld { public static void main(String[] args) { System.out.println(\"Hello World\"); } }"
        annotation.trainedTime = datetime.datetime.now()
        annotation.save()

        
        