from hack3rz_test import Hack3rzTest
from src.repositories.annotation import AnnotationRepository
import time

annotation_repository = AnnotationRepository()

class RepositoriesTest(Hack3rzTest):

    def test_annotation_find_training_data(self): # add function for every function
        """Tests if find_training_data() returns training data for correct number of entries for the "java" language.
        
        """
        lang_name = "java"
        training_data = annotation_repository.find_training_data(lang_name)
        self.assertEqual(len(training_data), 10)

    def test_annotation_update_trained_time(self):
        """Tests if find_training_data() returns training data for correct number of entries for the "python3" language.
        Additionally, update_trained_time() is tested indirectly. When update_trained_time() is executed successfully, the 
        fetched entries will be marked with a timestamp. This implies when trying to fetch the data again the return value must
        be 0 since there are no entries for training purposes left. 
        
        """
        lang_name = "python3"
        training_data = annotation_repository.find_training_data(lang_name)
        self.assertEqual(len(training_data), 10)
        annotation_repository.update_trained_time(training_data)
        training_data = annotation_repository.find_training_data(lang_name)
        self.assertEqual(len(training_data), 0)

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