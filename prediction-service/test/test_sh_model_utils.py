import os
import time

from hack3rz_test import Hack3rzTest
from src.util.SHModelUtils import SHModel


class SHModelUtilsTest(Hack3rzTest):
    def test_model_can_be_initiated_from_internal_store(self):
        lang = "JAVA"

        # create the model locally on the disk
        SHModel(lang.lower(), os.environ.get('MODEL_NAME'))

        # persist model to database
        self.save_sh_model_to_db(lang, 0.1234)
        time.sleep(3)

        # load model from db
        model = self.model_repository.get_or_fetch_model(lang.upper())

        # instantiate SHModel with model from db
        sh_model = SHModel(lang.lower(), os.environ.get('MODEL_NAME'), model.file)

        # we don't need any assertion here since SHModel will raise an exception if the above
        # statement failed
