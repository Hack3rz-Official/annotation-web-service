import json
from unittest.mock import patch
from hack3rz_test import Hack3rzTest
from src.models.annotation import Annotation, AnnotationKey
from src.services.training import improve_model, data_preprocessing, split_data, shuffle_data, compute_accuracy, train
from src.util.SHModelUtils import SHModel
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


    @patch('src.util.SHModelUtils.SHModel.finetune_on')
    def test_train(self, finetune_on_mock):
        finetune_on_mock.return_value = 1

        best_sh_model = SHModel("java", "test_best")
        X, T = super().load_test_X_T("java")
        epochs = 10

        train(best_sh_model, X, T, epochs)
        
        num_of_samples = X.shape[0]
        number_of_finetune_function_calls = epochs*num_of_samples
        self.assertIsNot(number_of_finetune_function_calls, 0)
        self.assertEqual(finetune_on_mock.call_count, number_of_finetune_function_calls)
    

    @patch('src.services.training.compute_accuracy')
    @patch('src.services.training.train')
    def test_improve_model_do_nothing(self, train_mock, compute_accuracy_mock):
        # skip train method execution
        train_mock.return_value = []
        # cur_acc is 10, new_acc is 5
        compute_accuracy_mock.side_effect = [10, 5]
       
        X, T = super().load_test_X_T("java")
        improve_model(X, T, "java")

        best_db_model = self.model_repository.find_best_model("java")
        self.assertIsNone(best_db_model)

    @patch('src.services.training.compute_accuracy')
    @patch('src.services.training.train')
    def test_improve_model_update_best_model(self, train_mock, compute_accuracy_mock):
        # skip train method execution
        train_mock.return_value = []
        # cur_acc is 5, new_acc is 10
        compute_accuracy_mock.side_effect = [5, 10]

        X, T = super().load_test_X_T("java")
        improve_model(X, T, "java")

        best_db_model = self.model_repository.find_best_model("java")
        self.assertIsNotNone(best_db_model)
        self.assertEquals(best_db_model.accuracy, 10)
    

    def test_annotation(self):
        annotation = Annotation()
        annotation.key = AnnotationKey(language="JAVA", lexingTokens=[1, 2, 3])
        annotation.sourceCode = "public class HelloWorld { public static void main(String[] args) { System.out.println(\"Hello World\"); } }"
        annotation.highlightingTokens = [1, 2, 3]
        annotation.highlightingCode = "public class HelloWorld { public static void main(String[] args) { System.out.println(\"Hello World\"); } }"
        annotation.trainedTime = datetime.datetime.now()
        annotation.save()

        
        
