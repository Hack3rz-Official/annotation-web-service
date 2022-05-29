from hack3rz_test import Hack3rzTest
from src.model.model import Model

class ModelTest(Hack3rzTest):
    def test_model_validation_exception_with_lowercase_language(self):
        wrong_language = "python3"  # lowercase is not allowed
        self.assertRaises(Exception, Model(language=wrong_language))

    def test_model_validation_exception_with_unsupported_language(self):
        wrong_language = "go"  # go is not allowed
        self.assertRaises(Exception, Model(language=wrong_language))


