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
        """Loads java data to test the data_preprocessing function. Should split the lexing and highlighting tokens & separates them.
        Then it will be asserted that neither of X or T are empty and both arrays are np.ndarrays (important for subsequent steps).
        
        Args: 
            training_data represents fetched training data from the db.
        
        """
        training_data = self.annotation_repository.find_data_to_train_with("java")
        X, T = data_preprocessing(training_data)
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(T, np.ndarray)
        self.assertNotEqual(X.size, 0)
        self.assertNotEqual(T.size,0)


    def test_split_data(self):
        """Tests for a correct data split in training and validation data. After the split it will be asserted that 
        the shapes are correct and from same size for X_train, T_train, X_val, T_val.

        Args:
            training_data represents fetched training data from the db.

        Returns:
            4 arrays with default split of 0.8 training & 0.2 validation data
        
        """
        training_data = self.annotation_repository.find_data_to_train_with("java")
        X, T = data_preprocessing(training_data)
        X_train, X_val, T_train, T_val = split_data(X, T, train_percentage=0.8)
        self.assertEqual(X_train.shape[0], T_train.shape[0])
        self.assertEqual(X_val.shape[0],T_val.shape[0])

    @patch('src.util.SHModelUtils.SHModel.predict')
    def test_compute_accuracy_valid(self, predict_mock):
        """Tests accuracy computation while mocking the return value of the predict function. Since 10 values are inside
        the training and the testing array, with only one deviation the logical return value of the compute_accuracy value
        must be 0.9.

        Args:
            predict_mock which is an array of dimension 1x10 and can be used to compute accuracy.
            best_sh_model which is the current SHModel which is in use by the prediction service and two arrays, training and tesing set.
        
        Returns:
            Float number in range [0,1].
        
        """
        X = np.array([[1], [1], [1], [1],[1],[1],[1],[1],[1],[1]])
        T = np.array([[1], [2], [1], [1],[1],[1],[1],[1],[1],[1]])
        predict_mock.side_effect = [[1], [1], [1], [1],[1],[1],[1],[1],[1],[1]]
        best_sh_model = SHModel("java", "test_best")
        ratio = compute_accuracy(best_sh_model, X, T)
        self.assertEqual(ratio, 0.9)
        self.assertTrue(0 <= ratio <= 1)
    
    def test_compute_accuracy_invalid(self):
        """Tests if an assertion error is raised by the compute_accuracy function if the two arrays are not of the same shape.
        """
        X = np.array([[1], [1], [1], [1],[1],[1],[1],[1],[1],[1]])
        T = np.array([[1], [2], [1], [1],[1],[1],[1],[1],[1]])
        best_sh_model = SHModel("java", "test_best")
        self.assertRaises(AssertionError,compute_accuracy,best_sh_model, X,T)
        

    def test_shuffle_data(self):
        """Tests if the input and ouput arrays are not equal after calling the shuffle_data function. Before the
        shuffeling the data_preprocessing function is called to split the data into training and testing data. 

        Args:
            training_data which are lexing and highlighting tokens from the aws_test db.

        Returns:
            Two shuffled arrays.
        
        """
        training_data = self.annotation_repository.find_data_to_train_with("java")
        X,T = data_preprocessing(training_data)
        X_shuff,T_shuff = shuffle_data(X,T)
        self.assertFalse(np.array_equal(X,X_shuff))
        self.assertFalse(np.array_equal(T,T_shuff))


    @patch('src.util.SHModelUtils.SHModel.finetune_on')
    def test_train(self, finetune_on_mock):
        """Tests the training process. Mocks a return value of the finetune_on function (1).
        Since its difficult to test the actual training process, we count the number of finetune_on calls 
        the model is generating during the process. The seeked number should be batch * number of samples. If the function is called
        batch * number of samples times then the test was successful. 

        Args:
            finetune_mock is an integer 1 which is used for the above explained purposes.
            best_sh_model which is a newly instantiated SHModel, a training set with training points and targets and a fixed number of
            epochs (default is 10).

        Returns:
            Array with losses (if assigned)

        """
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
        """Test for the case where a model (fetched from db) is trained and compared with the one in use (from prediction
        service). In this case the fetched model`s accuary is NOT higher than the one in use and therefore the current model
        is kept while the fetched model is discarded. The whole test case is built indirectly. We fetch before and after
        the improve_model() function the same amount of training_data (10, which is the number of entries when aws_test db is 
        instantiated). Consequently, this means that the new accuray is lower (5) than the current acccuracy (10) and there is no
        change of models. Evenutally, this implies that the training data is not marked as "used for training" and thus 
        the desired state is fact.

        Args:
            train_mock which is an empty array. compute_accuracy_mock which is an array with two values.

        """
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
        """Test for the case where a model (fetched from db) is trained and compared with the one in use (from prediction
        service). In this case the fetched model`s accuary is higher than the one in use and therefore the current model
        is discared and the new one saved to the current repository. The whole test case is built indirectly. We fetch before and after
        the improve_model() function the same amount of training_data (10, which is the number of entries when aws_test db is 
        instantiated). Consequently, this means that the new accuray is higher (10) than the current acccuracy (6) and there is a
        change of models. Evenutally, this implies that the training data is marked as "used for training" and thus does not appear
        as training_data anymore when fetched from the db via the function find_training_data.

        Args:
            train_mock which is an empty array. compute_accuracy_mock which is an array with two values.

        """
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

    
        
        