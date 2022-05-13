import os
from flask_restx import Resource, Namespace, fields, reqparse
from flask import abort
from src.util.SHModelUtils import SHModel
from src.repository.model import ModelRepository
import logging

logger = logging.getLogger('waitress')
api = Namespace("prediction", description="Prediction operations")

prediction_response_dto = api.model("PredictionResponseDTO", {
    "h_code_values": fields.List(fields.Integer)
})

prediction_parser = reqparse.RequestParser()
prediction_parser.add_argument(
    'lang_name',
    type=str,
    required=True,
    choices=('java', 'python3', 'kotlin'),
    help='Bad choice: Only "java", "python3", "kotlin" are currently supported.'
)
prediction_parser.add_argument(
    'tok_ids',
    type=int, 
    action='append',
    required=True,
    help='Bad choice: Use a list'
)

@api.route("")
class PredictionController(Resource):

    @api.expect(prediction_parser)
    @api.marshal_with(prediction_response_dto)
    def post(self):
        model_repository = ModelRepository()
        data = prediction_parser.parse_args()
        lang = data['lang_name']
        for tok_id in data["tok_ids"]:
            if not isinstance(tok_id, int):
                abort(400, 'only integers are allowed')
        try:
            model = model_repository.get_or_fetch_model(lang.upper())
            if model is None:
                logger.debug(F"No model for lang {lang} found. Initiating new model.")
                sh_model = SHModel(lang, os.environ.get('MODEL_NAME'))
            else:
                logger.debug(F"Using {lang} model with createdTime: {model.createdTime} and accuracy: {model.accuracy}")
                sh_model = SHModel(lang, os.environ.get('MODEL_NAME'), model.file)

            # TODO: potential performance boost if model is not re-instantiated and setup for every request
            sh_model.setup_for_prediction()
            values = sh_model.predict(data['tok_ids'])
            model_repository.async_check_for_better_model(lang.upper())
            return {'h_code_values': values}
        except Exception as e:
            logger.error("Model error: " + str(e))
            abort(500, "Model error: " + str(e))
