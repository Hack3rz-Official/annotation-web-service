import os
from flask_restx import Resource, Namespace, fields, reqparse
from flask import abort
from src.util.SHModelUtils import SHModel

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
        data = prediction_parser.parse_args()
        for tok_id in data["tok_ids"]:
            if not isinstance(tok_id, int):
                abort(400, 'only integers are allowed')
        try:
            model = SHModel(data['lang_name'], os.environ.get('MODEL_NAME'))
            model.setup_for_prediction()
            return {'h_code_values': model.predict(data['tok_ids'])}
        except Exception as e:
            abort(500, "Model error: " + str(e))
