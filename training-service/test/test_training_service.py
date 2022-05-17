import numpy as np
from unittest.mock import patch
from hack3rz_test import Hack3rzTest
from src.service.training import improve_model, data_preprocessing, split_objects, shuffle_data, compute_accuracy, train
from src.util.SHModelUtils import SHModel

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


    def test_split_objects(self):
        """Tests for a correct data split of an annotations array. After the split it will be asserted that 
        the shapes are correct, respectively according to the desired train_percentage split. Furthermore, we split the array with annotations
        for training and testing purposes into two arrays (data and labels) to ensure that the correct data and labels are used for training
        and validation purposes and that we do not mix them. 

        Args:
            training_data represents fetched training data from the db. train_percentage is a float between 0-1

        Returns:
            2 arrays with default split of 0.8 training & 0.2 validation data
        
        """
        annotations = self.annotation_repository.find_data_to_train_with("java")
        train_percentage = 0.8
        annotations_train, annotations_val = split_objects(annotations, train_percentage)
        
        # test data distinction
        for annotation_train in annotations_train:
            for annotation_val in annotations_val:
                self.assertNotEquals(annotation_train.key, annotation_val.key)
        
        self.assertEqual(len(annotations_train), np.ceil(len(annotations)*train_percentage))
        self.assertEqual(len(annotations_val), np.ceil(len(annotations)*(1-train_percentage)))
        

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
        X, T = data_preprocessing(training_data)
       
        X_shuff, T_shuff = shuffle_data(X, T)
        
        self.assertFalse(np.array_equal(X, X_shuff))
        self.assertFalse(np.array_equal(T, T_shuff)) 
        
        data_pairs = list(zip(X, T))
        self.assertEquals(len(X), len(T), len(data_pairs))
        for i in range(len(X_shuff)):
            # check if x and t still matches after shuffeling
            self.assertIn((X_shuff[i], T_shuff[i]), data_pairs)
            
    @patch('src.util.SHModelUtils.SHModel.finetune_on')
    def test_train_early_stopping(self, finetune_on_mock):
        """Tests the training process which must end in an early stopping due to entering the break out condition.  The Mocks return values of the finetune_on() function.
        Since its difficult to test the actual training process, we count the number of finetune_on calls  the model is generating during the process. 
        The seeked number should be a_len*5 (40) since after this amount of iterations the average loss of the current epoch equals the average loss of the previous epoch.

        Args:
            finetune_mock which is an array of 10*a_len values (80) floats is used for the above explained purposes.
            best_sh_model which is a newly instantiated SHModel, a training set with training points and targets and a fixed number 
            of epochs (10).

        Returns:
            Array with losses (if assigned)

        """
        best_sh_model = SHModel("java", "test_best")
        annotations = self.annotation_repository.find_data_to_train_with("java")
        annotations_train, _ = split_objects(annotations)
        X_train, T_train = data_preprocessing(annotations_train)   
        a_len = len(annotations_train)
        epochs = 10 
        
        finetune_on_mock.side_effect = [1] * a_len + [0.9] * a_len + [0.8] * a_len + [0.5] * a_len + [0.5] * a_len + [0.5] * a_len + [0.5] * a_len + [0.5] * a_len + [0.5] * a_len + [0.5] * a_len
        train(best_sh_model, X_train, T_train, epochs=epochs)
        
        # stop after 5 epochs due to loss convergence
        self.assertEqual(finetune_on_mock.call_count, a_len * 5)
        

    @patch('src.util.SHModelUtils.SHModel.finetune_on')
    def test_train_no_early_stopping(self, finetune_on_mock):
        """Tests the training process. In contrast to the above test, the train process should not be terminated by the early stopping but by reaching 
        the maximum amount of epochs (10).
        Since its difficult to test the actual training process, we count the number of finetune_on calls 
        the model is generating during the process. The seeked number should be 10*a_len (80) since after iterating through all the epochs the number of function calls 
        must be 80. 
        
        Args:
            finetune_mock which is an array of ten floats is used for the above explained purposes.
            best_sh_model which is a newly instantiated SHModel, a training set with training points and targets and a fixed number of 20
            epochs (default is 10).

        Returns:
            Array with losses (if assigned)

        """
        best_sh_model = SHModel("java", "test_best")
        annotations = self.annotation_repository.find_data_to_train_with("java")
        annotations_train, _ = split_objects(annotations)
        X_train, T_train = data_preprocessing(annotations_train)  
        a_len = len(annotations_train)
        epochs = 10 
        
        finetune_on_mock.side_effect = [1] * a_len + [0.9] * a_len + [0.8] * a_len + [0.7] * a_len + [0.6] * a_len + [0.5] * a_len + [0.4] * a_len + [0.3] * a_len + [0.2] * a_len + [0.1] * a_len
        train(best_sh_model, X_train, T_train, epochs=epochs)
        
        self.assertEqual(finetune_on_mock.call_count, a_len * epochs)
    
    @patch('src.service.training.FALLBACK_ACCURACY', 100)
    @patch('src.service.training.compute_accuracy')
    @patch('src.service.training.train')
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
        # new_acc is 5
        compute_accuracy_mock.return_value = 5
        
        # prepare and run function
        training_data = self.annotation_repository.find_data_to_train_with("java")
        annotations_train, annotations_val = split_objects(training_data)
        improve_model(annotations_train, annotations_val, "java")
        
        # test model
        best_db_model = self.model_repository.find_best_model("java")
        self.assertIsNone(best_db_model)
        
        # test annotations
        training_data = self.annotation_repository.find_data_to_train_with("java")
        
        # test db has 10 test annotations initially loaded per language
        self.assertEqual(10, len(training_data))
    
    @patch('src.service.training.FALLBACK_ACCURACY', 9)
    @patch('src.service.training.compute_accuracy')
    @patch('src.service.training.train')
    def test_improve_model_update_best_model_and_flag_used_data(self, train_mock, compute_accuracy_mock):
        """Test for the case where a model (fetched from db) is trained and compared with the one in use (from prediction
        service). In this case the fetched model`s accuary is higher than the one in use and therefore the current model
        is discared and the new one saved to the current repository. The whole test case is built indirectly. We fetch before
        the improve_model() function training_data (10, which is the number of entries when aws_test db is 
        instantiated). Afterwards we fetch again training_data but this time the return value is 0 since the training data is marked as 
        "used for training" . Consequently, this means that the new accuray is higher (10) than the current acccuracy (6) and there is a
        change of models.

        Args:
            train_mock which is an empty array. compute_accuracy_mock which is an array with two values.

        """
        # create functions mocks
        # skip train method execution
        train_mock.return_value = []
        # new_acc is 10
        compute_accuracy_mock.return_value = 10

        # prepare and run functions
        training_data = self.annotation_repository.find_data_to_train_with("java")
        annotations_train, annotations_val = split_objects(training_data)
        improve_model(annotations_train, annotations_val, "java")

        best_db_model = self.model_repository.find_best_model("java")
        self.assertIsNotNone(best_db_model)
        
        training_data = self.annotation_repository.find_data_to_train_with("java")
        self.assertEquals(best_db_model.accuracy, 10)
        self.assertEquals(0, len(training_data))
