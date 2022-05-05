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
        training_data = self.annotation_repository.find_data_to_train_with("java")
        X, T = data_preprocessing(training_data)
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(T, np.ndarray)
        self.assertNotEqual(X.size, 0)
        self.assertNotEqual(T.size,0)


    def test_split_data(self):
        training_data = self.annotation_repository.find_data_to_train_with("java")
        X, T = data_preprocessing(training_data)
        X_train, X_val, T_train, T_val = split_data(X, T, train_percentage=0.8)
        self.assertEqual(X_train.shape[0], T_train.shape[0])
        self.assertEqual(X_val.shape[0],T_val.shape[0])

    @patch('src.util.SHModelUtils.SHModel.predict')
    def test_compute_accuracy_valid(self, predict_mock):
        X = np.array([[1], [1], [1], [1],[1],[1],[1],[1],[1],[1]])
        T = np.array([[1], [2], [1], [1],[1],[1],[1],[1],[1],[1]])
        predict_mock.side_effect = [[1], [1], [1], [1],[1],[1],[1],[1],[1],[1]]
        best_sh_model = SHModel("java", "test_best")
        ratio = compute_accuracy(best_sh_model, X, T)
        self.assertEqual(ratio, 0.9)
    
    @patch('src.util.SHModelUtils.SHModel.predict')
    def test_compute_accuracy_invalid(self, predict_mock):
        X = np.array([[1], [1], [1], [1],[1],[1],[1],[1],[1],[1]])
        T = np.array([[1], [2], [1], [1],[1],[1],[1],[1],[1]])
        best_sh_model = SHModel("java", "test_best")
        self.assertRaises(AssertionError,compute_accuracy,best_sh_model, X,T)
        

    def test_shuffle_data(self):
        training_data = self.annotation_repository.find_data_to_train_with("java")
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
        # create functions mocks
        # skip train method execution
        train_mock.return_value = []
        # cur_acc is 10, new_acc is 5
        compute_accuracy_mock.side_effect = [10, 5]
        
        # prepare and run function
        training_data = self.annotation_repository.find_data_to_train_with("java")
        X, T = super().load_test_X_T("java")
        improve_model(X, T, "java", training_data)
        
        # test model
        best_db_model = self.model_repository.find_best_model("java")
        self.assertIsNone(best_db_model)
        
        # test annotations
        training_data = self.annotation_repository.find_data_to_train_with("java")
        # test db has 10 test annotations initially loaded per language
        self.assertEqual(10, len(training_data))

    @patch('src.services.training.compute_accuracy')
    @patch('src.services.training.train')
    def test_improve_model_update_best_model(self, train_mock, compute_accuracy_mock):
        # create functions mocks
        # skip train method execution
        train_mock.return_value = []
        # cur_acc is 5, new_acc is 10
        compute_accuracy_mock.side_effect = [5, 10]

        # prepare and run functions
        training_data = self.annotation_repository.find_data_to_train_with("java")
        X, T = super().load_test_X_T("java")
        improve_model(X, T, "java", training_data)

        best_db_model = self.model_repository.find_best_model("java")
        self.assertIsNotNone(best_db_model)
        
        training_data = self.annotation_repository.find_data_to_train_with("java")
        self.assertEquals(best_db_model.accuracy, 10)
        self.assertEquals(0, len(training_data))

    
        
        