#!/usr/bin/env python3
from flask_mongoengine import MongoEngine
from unittest import TestCase, mock
import os
import warnings
import glob
from app import create_app
from src.model.model import Model
from src.repository.model import ModelRepository
from src.util.SHModelHelper import get_model_path


class Hack3rzTest(TestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()

        warnings.simplefilter('ignore', category=DeprecationWarning)
        
        self.env_patcher = mock.patch.dict(os.environ, {
            "MONGO_USERNAME": "hack3rz",
            "MONGO_PASSWORD": "palm_tree_poppin_out_the_powder_blue_sky",
            "MONGO_DATABASE_NAME": "aws_test",
            "MONGO_PORT": "27017",
            "MONGO_HOST": "localhost",
            "MONGO_AUTH_DATABASE": "admin",
            "TRAINING_BATCH_SIZE": "100",
            "MODEL_NAME": "test_best"
        }, clear=True)
        self.env_patcher.start()
        
        self.app = create_app()
        self.app.testing = True
        self.db = MongoEngine()
        self.model_repository = ModelRepository()
    
    # called before running every test
    def setUp(self):
        assert self.db.get_db().name == "aws_test"

        # TODO drop all collections at once?
        Model.drop_collection()

    def save_sh_model_to_db(self, lang_name, accuracy):
        """
        Loads the model from the disk (if it exists) and saves it to the database
        :param lang_name: string with the language of the model
        :param accuracy: float with the accuracy of the model
        """
        print("[TRAIN] New Model saved from directory to DB ", flush=True)
        model = Model(language=lang_name, accuracy=accuracy)
        model_path = get_model_path(lang_name)
        try:
            with open(model_path, "rb") as binary_file:
                model.file.put(binary_file)
        except FileNotFoundError:
            print(F"[TRAIN] Error: No model with path {model_path} found on disk.")
        model.save()

    @staticmethod
    def delete_test_models():
        file_list = glob.glob('*test_best.pt')
        for file_path in file_list:
            try:
                os.remove(file_path)
                print("Deleting file: ", file_path)
            except:
                print("Error while deleting file: ", file_path)

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        self.delete_test_models()
        self.env_patcher.stop()


