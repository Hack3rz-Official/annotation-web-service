import unittest
import azure.functions as func
import json

from predict import main

# execute with: python -m unittest tests/predict_test.py
class TestPredict(unittest.TestCase):

    def test_predict_java(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/predict',
            body=json.dumps({
                'lang_name': 'java',
                'tok_ids': [42, 42, 75, 76]
            }).encode('utf8')
        )

        response = main(request)

        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert len(body['h_code_values']) == 4


    def test_predict_python3(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/predict',
            body=json.dumps({
                'lang_name': 'python3',
                'tok_ids': [42, 42, 75, 76]
            }).encode('utf8')
        )

        response = main(request)

        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert len(body['h_code_values']) == 4

    def test_predict_kotlin(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/predict',
            body=json.dumps({
                'lang_name': 'kotlin',
                'tok_ids': [42, 42, 75, 76]
            }).encode('utf8')
        )

        response = main(request)

        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert len(body['h_code_values']) == 4

    def test_predict_invalid_body(self):
        request = func.HttpRequest(
            method='GET',
            url='/api/predict',
            body="no json"
        )

        response = main(request)

        assert response.status_code == 400
        assert response.get_body().decode() == "Invalid body, please provide json"

    def test_predict_unsupported_language(self):
        lang = "go"
        request = func.HttpRequest(
            method='GET',
            url='/api/predict',
            body=json.dumps({
                'lang_name': lang,
                'tok_ids': [42, 42, 75, 76]
            }).encode('utf8')
        )

        response = main(request)

        assert response.status_code == 400
        assert response.get_body().decode() == f"{lang} is an unsupported programming language"



