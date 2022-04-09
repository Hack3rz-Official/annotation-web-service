import logging
from model.SHModelUtils import SHModel
from flask import Flask, Response, request 
import json

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    supported_languages = ["java", "python3", "kotlin"]
    logging.info('Python HTTP trigger function processed a request.')

    # deserialize
    try:
        req_body = request.get_json()
        lang_name = req_body.get('lang_name')
        tok_ids = req_body.get('tok_ids')
    except Exception as e:
        logging.error("Invalid body, not json" + str(e))
        return Response("Invalid body, please provide json", status=400)

    # handle unsupported languages
    if lang_name not in supported_languages:
        logging.error("Unsupported language")
        return Response(f"{lang_name} is an unsupported programming language", status=400)

    try:    
        # predict
        model = SHModel(lang_name, "curr")
        model.setup_for_prediction()
        res = model.predict(tok_ids)
        return Response(json.dumps({'h_code_values': res}))
    except Exception as e:
        logging.error("Model error: " + str(e))
        return Response("Model error: " + str(e), status=500)
    

if __name__ == "__main__":
    app.run(debug=True)
