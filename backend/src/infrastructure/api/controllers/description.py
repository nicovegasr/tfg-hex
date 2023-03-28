import json
from flask import make_response, request
from src.aplication.usecases.get_algorithm_description import get_algorithm_description

def description():
    try:
        algorithm_name = request.args.get("algorithm_name")
        description: list = json.dumps(get_algorithm_description(algorithm_name))
        return make_response(description, 200)
    except ValueError as Error:
        return make_response(str(Error), 404)