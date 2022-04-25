from flask import Blueprint, jsonify
from src.services.training import train_models

training_blueprint = Blueprint(name="training", import_name=__name__)

@training_blueprint.route('/', methods=['GET'])
def main():
    """Train syntax highlighting models for all supported languages
    ---
    definitions:
      Output:
        type: object
        properties:
          msg:
            type: string
    responses:
      200:
        description: An output message
        schema:
          $ref: '#/definitions/Output'
    tags:
        - Training
    """
    msg = train_models()
    output = {"msg": msg}
    return jsonify(output)