from hack3rz_test import Hack3rzTest
from src.repository.annotation import AnnotationRepository
import time
import datetime
from src.service.training import split_objects

annotation_repository = AnnotationRepository()

class RepositoriesTest(Hack3rzTest):

    def test_annotation_find_data_to_train_with(self): # add function for every function
        """Tests if find_training_data_to_train_with() returns training data for correct number of entries for the "java" 
        language.
        
        """
        lang_name = "java"
        training_data = annotation_repository.find_data_to_train_with(lang_name)
        self.assertEqual(len(training_data), 10)

    def test_annotation_update_trained_time(self):
        """Tests if find_training_data_to_train_with() returns training data for correct number of entries for the "python3" language.
        Additionally, update_trained_time() is tested indirectly. When update_trained_time() is executed successfully, the 
        fetched entries will be marked with a timestamp. This implies when trying to fetch the data again the return value must
        be 0 since there are no entries for training purposes left. 
        
        """
        lang_name = "python3"
        training_data = annotation_repository.find_data_to_train_with(lang_name)
        self.assertEqual(len(training_data), 10)
        time = datetime.datetime.now()
        annotation_repository.update_trained_time(training_data, time)  
        training_data = annotation_repository.find_data_to_train_with(lang_name)
        self.assertEqual(len(training_data), 0)


    def test_annotation_find_validation_data(self):
        """Tests if find_validation_data() returns validation data for correct number of entries for the "java" 
        language.
        
        """
        lang_name = "java"
        validation_data = annotation_repository.find_validation_data(lang_name)
        self.assertEqual(len(validation_data), 0)


    def test_annotation_update_validated_time(self):
        """Tests if find_validation_data() returns validation data for correct number of entries for the "python3" language.
        To do so, we first need to flag some data on the aws_test db as validation data. Additionally, update_validated_time() is tested indirectly. When update_validated_time() is executed successfully, the 
        fetched entries will be marked with a timestamp. This implies when trying to fetch the data again the return value must
        be 10 since we always want to validate on a global set of validation data (in contrast to the find_data_to_train_with() function).
        
        """
        lang_name = "python3"
        training_data = annotation_repository.find_data_to_train_with(lang_name)
        validation_data = annotation_repository.find_validation_data(lang_name)

        # should be an empty array since per default no validation data is on the aws data base
        self.assertEqual(len(training_data), 10)
        self.assertEqual(len(validation_data), 0)

        # fetch training data objects (10) and mark them as validation data
        time = datetime.datetime.now()
        annotation_repository.update_validated_time(training_data, time)
        validation_data = annotation_repository.find_validation_data(lang_name)
        self.assertEqual(len(validation_data), len(training_data))
        
    
    def test_annotation_update_trained_time_and_validation_time(self):
        """Tests if the update functions of the annotation entries are working simultanously & successfully. Since the function find_data_to_train_with() 
        fetches an array with 10 annotation objects and the split_objects() splits the array into two arrays, annotations_train shoud have length 8 and 
        annotations_val shoud have length 2. Furthermore after updating their trainedTime or validatedTime field the find functions should return 0 for 
        the training_data array and 2 for the validation_data. This design is chosen because we want always to validate our models on the biggest possible
        validation set and therefore the validation set will grow with the number of entries in our db while the training data is always depending on the 
        MIN_BATCH_SIZE variable. 

        """
        lang_name = "python3"
        training_data = annotation_repository.find_data_to_train_with(lang_name)
        annotations_train, annotations_val = split_objects(training_data)
        
        self.assertEqual(len(annotations_train), 8)
        self.assertEqual(len(annotations_val), 2)
        
        time = datetime.datetime.now()
        annotation_repository.update_trained_time(annotations_train, time) 
        annotation_repository.update_validated_time(annotations_val, time) 
         
        training_data = annotation_repository.find_data_to_train_with(lang_name)
        validation_data = annotation_repository.find_validation_data(lang_name)
        self.assertEqual(len(training_data), 0)
        self.assertEqual(len(validation_data), 2)
        

    def test_model_find_best_model(self):
        """Tests if find_best_model() is actually returning the desired model which is in this test case the model with the accuracy of
        0.1234. 

        """
        test_acc = 0.1234
        super().save_sh_model_to_db("python3", test_acc)
        model = self.model_repository.find_best_model("python3")
        self.assertEqual(test_acc, model.accuracy)

    def test_fetch_newest_model(self):
        """Tests if find_best_model() is returning the model with the highest accuary if there are more than one model on the 
        aws_test db. 
        
        """
        test_acc1 = 0.123
        test_acc2 = 0.789
        super().save_sh_model_to_db("python3", test_acc1)
        time.sleep(3)
        super().save_sh_model_to_db("python3", test_acc2)
        model = self.model_repository.find_best_model("python3")
        self.assertEqual(test_acc2, model.accuracy)