from hack3rz_test import Hack3rzTest
from src.repositories.annotation import AnnotationRepository

annotation_repository = AnnotationRepository()

class RepositoriesTest(Hack3rzTest):

    def test_annotation_find_training_data(self):
        super().load_training_test_data()

        lang_name = "java"
        training_data = annotation_repository.find_training_data(lang_name)
        self.assertEqual(len(training_data), 10)

    def test_annotation_update_trained_time(self):
        super().load_training_test_data()

        lang_name = "python3"
        training_data = annotation_repository.find_training_data(lang_name)
        self.assertEqual(len(training_data), 10)
        annotation_repository.update_trained_time(training_data)
        training_data = annotation_repository.find_training_data(lang_name)
        self.assertEqual(len(training_data), 0)

    def test_model_find_best_model(self):
        pass

    def test_model_save(self):
        pass
