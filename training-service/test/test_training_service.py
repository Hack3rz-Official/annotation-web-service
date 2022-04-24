import json
from unittest.mock import patch
from hack3rz_test import Hack3rzTest
from src.models.annotation import Annotation, AnnotationKey
from src.services.training import improve_model, data_preprocessing, split_data, shuffle_data, compute_accuracy
import datetime
import numpy as np

# run within the test folder the following commoand to execute file
# run with: python3 -m unittest test_training_service.py

class TrainingServiceTest(Hack3rzTest):

    def test_data_preprocessing(self):  
        training_data = self.annotation_repository.find_training_data("java")
        X, T = data_preprocessing(training_data)
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(T, np.ndarray)
        self.assertNotEqual(X.size, 0)
        self.assertNotEqual(T.size,0)


    def test_split_data(self):
        training_data = self.annotation_repository.find_training_data("java")
        X, T = data_preprocessing(training_data)
        X_train, T_train, X_val, T_val = split_data(X, T, train_percentage=0.8)
        self.assertEqual(X_train.shape[0], T_train.shape[0])
        self.assertEqual(X_val.shape[0],T_val.shape[0])

    def test_accuracy(self):
        pass

    def test_shuffle_data(self):
        training_data = self.annotation_repository.find_training_data("java")
        X,T = data_preprocessing(training_data)
        X_shuff,T_shuff = shuffle_data(X,T)
        self.assertFalse(np.array_equal(X,X_shuff))
        self.assertFalse(np.array_equal(T,T_shuff))




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

        
        