#!/usr/bin/env python3
from flask_mongoengine import MongoEngine
from unittest import TestCase, mock
import os
from app import create_app
from src.models.annotation import Annotation
from src.models.model import Model
from src.repositories.annotation import AnnotationRepository
from src.repositories.model import ModelRepository
from src.services.training import data_preprocessing
from src.util.SHModelHelper import SHModel
import json
import warnings

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

        self.app  = create_app()
        self.app.testing = True
        self.db = MongoEngine()
        self.annotation_repository = AnnotationRepository()
        self.model_repository = ModelRepository()
    
    # called before running every test
    def setUp(self):
        assert self.db.get_db().name == "aws_test"

        # TODO drop all collections at once?
        Annotation.drop_collection()
        Model.drop_collection()
        self.load_training_test_data()

    def save_sh_model_to_db(self,lang_name, accuracy):
        model = SHModel(lang_name, os.environ.get('MODEL_NAME'))
        print("[TRAIN] New Model saved from directory to DB ", flush=True)
        model = Model(language=lang_name, accuracy=accuracy)
        with open(lang_name + "_" + os.environ.get('MODEL_NAME') + ".pt", "rb") as binary_file:
            model.file.put(binary_file)
        model.save()


    def load_training_test_data(self):
        with open('annotations.json') as file:
            file_data = json.load(file)
            annotation_instances = [Annotation.from_json(json.dumps(annotation), created=True) for annotation in file_data]
            Annotation.objects.insert(annotation_instances, load_bulk=False)

    def load_test_X_T(self, lang_name):
        X, T = data_preprocessing(self.annotation_repository.find_training_data(lang_name))
        return X, T

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

        self.env_patcher.stop()