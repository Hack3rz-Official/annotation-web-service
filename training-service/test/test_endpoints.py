import json
from hack3rz_test import Hack3rzTest
from src.model.annotation import Annotation

# run all tests: python3 -m unittest
# run with: python3 -m unittest test_endpoints.py
class EndpointsTest(Hack3rzTest):

    def test_training_java(self):
        "Tests if the java model is accessible and responses with a status code of 200"
        with self.app.test_client() as client:
            response = client.put('/api/v1/training', json={
                'model': 'java'
            })
            self.assertEqual(response.status_code, 200)
            response_body = json.loads(response.get_data())
            self.assertIsInstance(response_body['msg'], str)

    def test_training_kotlin(self):
        "Tests if the kotlin model is accessible and responses with a status code of 200"
        with self.app.test_client() as client:
            response = client.put('/api/v1/training', json={
                'model': 'kotlin'
            })
            self.assertEqual(response.status_code, 200)
            response_body = json.loads(response.get_data())
            self.assertIsInstance(response_body['msg'], str)

    def test_training_python3(self):
        "Tests if the python3 model is accessible and responses with a status code of 200"
        with self.app.test_client() as client:
            response = client.put('/api/v1/training', json={
                'model': 'python3'
            })
            self.assertEqual(response.status_code, 200)
            response_body = json.loads(response.get_data())
            self.assertIsInstance(response_body['msg'], str)

    def test_training_all(self):
        "Tests if all the models are accessible and responses with a status code of 200"
        with self.app.test_client() as client:
            response = client.put('/api/v1/training', json={
                'model': 'all'
            })
            self.assertEqual(response.status_code, 200)
            response_body = json.loads(response.get_data())
            self.assertIsInstance(response_body['msg'], str)

    def test_training_invalid_model(self):
        "Tests if the status code 400 is returned if an invalid model is called"
        with self.app.test_client() as client:
            response = client.put('/api/v1/training', json={
                'model': 'any'
            })
            self.assertEqual(response.status_code, 400)

    def test_training_invalid_request(self):
        "Tests if the status code 400 is returned if an invalid request is placed."
        with self.app.test_client() as client:
            response = client.put('/api/v1/training', json={
                'test': 'test'
            })
            self.assertEqual(response.status_code, 400)
