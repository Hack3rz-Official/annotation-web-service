from src.services.training import train_models
from flask_restx import Resource, Namespace, fields, reqparse

api = Namespace("training", description="Item operations")

training_response_dto = api.model("TrainingResponseDTO", {
    "msg": fields.String
})

training_parser = reqparse.RequestParser()
training_parser.add_argument(
    'model',
    type=str,
    required=True,
    choices=('all', 'java', 'python3', 'kotlin'),
    help='Bad choice: Only "all", "java", "python3", "kotlin" are supported.'
)

@api.route("")
class TrainingController(Resource):

    @api.expect(training_parser)
    @api.marshal_with(training_response_dto)
    def put(self):
        data = training_parser.parse_args()
        msg = train_models(data['model'])
        return {"msg": msg}
