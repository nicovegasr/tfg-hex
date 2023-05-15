import json

from flask import make_response, request

from aplication.usecases.get_configuration_file import get_configuration_file
from aplication.usecases.get_algorithm_description import get_algorithm_description


def description():
    try:
        algorithm_name = request.args.get("algorithm_name")
        configuration_file = get_configuration_file(algorithm_name)
        description: list = json.dumps(get_algorithm_description(configuration_file))
        return make_response(description, 200)
    except ValueError as Error:
        return make_response(str(Error), 404)
