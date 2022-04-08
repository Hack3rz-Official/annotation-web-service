import json
import unittest

from app import app
app.testing = True

# run with: python3 -m unittest tests.py
class Tests(unittest.TestCase):

    def test_predict_java(self):
        with app.test_client() as client:
            response = client.post('/predict', json={
                'lang_name': 'java',
                'tok_ids': [42, 42, 75, 76]
            })
            self.assertEqual(response.status_code, 200)
            response_body = json.loads(response.get_data())
            self.assertTrue(len(response_body['h_code_values']) == 4)

    def test_predict_python3(self):
        with app.test_client() as client:
            response = client.post('/predict', json={
                'lang_name': 'python3',
                'tok_ids': [42, 42, 75, 76]
            })
            self.assertEqual(response.status_code, 200)
            response_body = json.loads(response.get_data())
            self.assertTrue(len(response_body['h_code_values']) == 4)

    def test_predict_kotlin(self):
        with app.test_client() as client:
            response = client.post('/predict', json={
                'lang_name': 'kotlin',
                'tok_ids': [42, 42, 75, 76]
            })
            self.assertEqual(response.status_code, 200)
            response_body = json.loads(response.get_data())
            self.assertTrue(len(response_body['h_code_values']) == 4)

    def test_predict_invalid_body(self):
        with app.test_client() as client:
            response = client.post('/predict', data='no json')
            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.get_data().decode() == "Invalid body, please provide json")

    def test_predict_unsupported_language(self):
        with app.test_client() as client:
            unsupported_lang = "go"
            response = client.post('/predict', json={
                'lang_name': unsupported_lang,
                'tok_ids': [42, 42, 75, 76]
            })
            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.get_data().decode() == f"{unsupported_lang} is an unsupported programming language")
