#!/usr/bin/env python3
from flask_mongoengine import MongoEngine
from unittest import TestCase, mock
import os
from app import create_app
from src.model.model import Model
from src.repository.model import ModelRepository
from src.util.SHModelUtils import SHModel
import warnings
import glob


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
        model = SHModel(lang_name, os.environ.get('MODEL_NAME'))
        print("[TRAIN] New Model saved from directory to DB ", flush=True)
        model = Model(language=lang_name, accuracy=accuracy)
        with open(lang_name + "_" + os.environ.get('MODEL_NAME') + ".pt", "rb") as binary_file:
            model.file.put(binary_file)
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


