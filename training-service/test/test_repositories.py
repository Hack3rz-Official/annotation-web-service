from hack3rz_test import Hack3rzTest
from src.repositories.annotation import AnnotationRepository
import time

annotation_repository = AnnotationRepository()

class RepositoriesTest(Hack3rzTest):

    def test_annotation_find_data_to_train_with(self): # add function for every function
        lang_name = "java"
        training_data = annotation_repository.find_data_to_train_with(lang_name)
        self.assertEqual(len(training_data), 10)

    def test_annotation_update_trained_time(self):
        lang_name = "python3"
        training_data = annotation_repository.find_data_to_train_with(lang_name)
        self.assertEqual(len(training_data), 10)
        annotation_repository.update_trained_time(training_data)
        training_data = annotation_repository.find_data_to_train_with(lang_name)
        self.assertEqual(len(training_data), 0)

    def test_model_find_best_model(self):
        test_acc = 0.1234
        super().save_sh_model_to_db("python3", test_acc)
        model = self.model_repository.find_best_model("python3")
        self.assertEqual(test_acc, model.accuracy)

    def test_fetch_newest_model(self):
        test_acc1 = 0.123
        test_acc2 = 0.789
        super().save_sh_model_to_db("python3", test_acc1)
        time.sleep(3)
        super().save_sh_model_to_db("python3", test_acc2)
        model = self.model_repository.find_best_model("python3")
        self.assertEqual(test_acc2, model.accuracy)