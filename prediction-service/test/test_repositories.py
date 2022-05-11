import os

from hack3rz_test import Hack3rzTest
import time

from src.util.SHModelUtils import SHModel


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
