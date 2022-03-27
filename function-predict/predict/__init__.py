import logging
from model.SHModelUtils import SHModel
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    supported_languages = ["java"]
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        logging.info('json error')
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )
    else:
        lang_name = req_body.get('lang_name')
        tok_ids = req_body.get('tok_ids')

    if lang_name not in supported_languages:
        return func.HttpResponse(
             f"{lang_name} is an unsupported programming language",
             status_code=400
        )

    model = SHModel(lang_name, "best")
    model.setup_for_prediction();
    res = model.predict(tok_ids);
    return func.HttpResponse(json.dumps({'h_code_values': res}))