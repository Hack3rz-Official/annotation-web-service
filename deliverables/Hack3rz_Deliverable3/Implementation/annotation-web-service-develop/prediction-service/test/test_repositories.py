from hack3rz_test import Hack3rzTest
import time

# run with: python3 -m unittest test_prediction.py
class RepositoriesTest(Hack3rzTest):

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
