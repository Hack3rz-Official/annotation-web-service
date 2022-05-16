#!/usr/bin/env python3
from flask_mongoengine import MongoEngine
from unittest import TestCase, mock
import os
from app import create_app
from src.model.annotation import Annotation
from src.model.model import Model
from src.repository.annotation import AnnotationRepository
from src.repository.model import ModelRepository
from src.util.SHModelHelper import SHModel
import json
import warnings

class Hack3rzTest(TestCase):

    @classmethod
    def setUpClass(self):
        """Sets up a db called aws_test for the test files in the test folder. Annotation and Model objects are instantiated
        since they will be used to either fetch training data or models from db.
        
        """
        super().setUpClass()

        warnings.simplefilter('ignore', category=DeprecationWarning)
        
        self.env_patcher = mock.patch.dict(os.environ, {
            "MONGO_USERNAME": "hack3rz",
            "MONGO_PASSWORD": "palm_tree_poppin_out_the_powder_blue_sky",
            "MONGO_DATABASE_NAME": "aws_test",
            "MONGO_PORT": "27017",
            "MONGO_HOST": "localhost",
            "MONGO_AUTH_DATABASE": "admin",
            "MIN_TRAINING_BATCH_SIZE": "100",
            "MODEL_NAME": "test_best"
        }, clear=True)
        self.env_patcher.start()

        self.app  = create_app()
        self.app.testing = True
        self.db = MongoEngine()
        self.annotation_repository = AnnotationRepository()
        self.model_repository = ModelRepository()
        
    def setUp(self):
        """
        Called before running a single test
        """
        assert self.db.get_db().name == "aws_test"
        Annotation.drop_collection()
        Model.drop_collection()
        self.load_training_test_data()

    def tearDown(self):
        """
        Called after running a single test
        """
        pass

    def save_sh_model_to_db(self,lang_name, accuracy):
        """Saves an SHModel to the db on the collection "models". 

        Args:
            Corresponding language name (string) of the model and its accuracy. Both args will be saved in a separate coloumn on the db.
        
        """
        model = SHModel(lang_name.lower(), os.environ.get('MODEL_NAME'))
        print("[TRAIN] New Model saved from directory to DB ", flush=True)
        model = Model(language=lang_name.upper(), accuracy=accuracy)
        with open(lang_name.lower() + "_" + os.environ.get('MODEL_NAME') + ".pt", "rb") as binary_file:
            model.file.put(binary_file)
        model.save()


    def load_training_test_data(self):
        """Populates db with test data which can be used for testing purposes. The data is fetched from the annotation.json
        file in the test folder and will be saved on the annotation collection.
        
        """
        with open('annotations.json') as file:
            file_data = json.load(file)
            annotation_instances = [Annotation.from_json(json.dumps(annotation), created=True) for annotation in file_data]
            Annotation.objects.insert(annotation_instances, load_bulk=False)

    @classmethod
    def tearDownClass(self):
        """Tears down whole class when called. Inherited method from TestCase.
        
        """
        super().tearDownClass()

        self.env_patcher.stop()
        
        Annotation.drop_collection()
        Model.drop_collection()
