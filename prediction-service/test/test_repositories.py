import os

from hack3rz_test import Hack3rzTest
import time

from src.util.SHModelUtils import SHModel
from src.repository.model import ModelRepository


class RepositoriesTest(Hack3rzTest):

    def test_model_find_best_model(self):
        test_acc = 0.1234
        lang = "PYTHON3"
        # create the model locally on the disk
        model = SHModel(lang.lower(), os.environ.get('MODEL_NAME'))
        super().save_sh_model_to_db(lang, test_acc)
        model = self.model_repository.find_best_model(lang)
        self.assertEqual(test_acc, model.accuracy)

    def test_fetch_newest_model(self):
        test_acc1 = 0.123
        test_acc2 = 0.789
        lang = "PYTHON3"
        # create the model locally on the disk
        model = SHModel(lang.lower(), os.environ.get('MODEL_NAME'))
        super().save_sh_model_to_db(lang, test_acc1)
        time.sleep(3)
        super().save_sh_model_to_db(lang, test_acc2)
        model = self.model_repository.find_best_model(lang)
        self.assertEqual(test_acc2, model.accuracy)

    def test_singleton_behavior(self):

        model_repository = ModelRepository()
        model_repository.reset()

        test_acc1 = 0.123
        lang = "PYTHON3"

        # create the model locally on the disk
        SHModel(lang.lower(), os.environ.get('MODEL_NAME'))
        self.save_sh_model_to_db(lang, test_acc1)
        time.sleep(3)

        # initially the model should be none
        self.assertIsNone(model_repository.get_models()[lang])

        # should fetch and return the best model
        model = model_repository.get_or_fetch_model(lang)
        self.assertIsNotNone(model)
        self.assertEqual(test_acc1, model.accuracy)

        # make sure other instance of repository still returns same model
        model_repository = ModelRepository()
        model = model_repository.get_models()[lang]
        self.assertIsNotNone(model)
        self.assertEqual(test_acc1, model.accuracy)

    def test_check_for_better_model(self):
        model_repository = ModelRepository()
        test_acc1 = 0.123
        test_acc2 = 0.789
        lang = "PYTHON3"

        # create the model locally on the disk
        SHModel(lang.lower(), os.environ.get('MODEL_NAME'))
        self.save_sh_model_to_db(lang, test_acc1)
        time.sleep(3)

        # should fetch and return the first model
        model1 = model_repository.get_or_fetch_model(lang)
        self.assertIsNotNone(model1)
        self.assertEqual(test_acc1, model1.accuracy)

        # save a second model with higher accuracy
        self.save_sh_model_to_db(lang, test_acc2)
        time.sleep(3)

        # should fetch and return the second model with higher accuracy
        model2 = model_repository.check_for_better_model(lang)
        self.assertIsNotNone(model2)
        self.assertEqual(test_acc2, model2.accuracy)

        # better model should be stored internally and returned on subsequent call
        best_model = model_repository.get_or_fetch_model(lang)
        self.assertEqual(test_acc2, best_model.accuracy)
