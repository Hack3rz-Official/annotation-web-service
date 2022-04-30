import json
from hack3rz_test import Hack3rzTest
from src.models.annotation import Annotation

# run all tests: python3 -m unittest
# run with: python3 -m unittest test_endpoints.py
class EndpointsTest(Hack3rzTest):

    def test_training(self):
        with self.app.test_client() as client:
            response = client.get('/api/v1/training/')
            self.assertEqual(response.status_code, 200)
            response_body = json.loads(response.get_data())
            self.assertIsInstance(response_body['msg'], str)
