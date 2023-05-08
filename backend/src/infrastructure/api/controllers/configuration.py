import json

from flask import make_response, request

from aplication.usecases.get_configuration_file import get_configuration_file


def configuration_file():
    try:
        algorithm_name = request.args.get("algorithm_name")
        configuration_file = get_configuration_file(algorithm_name)
        configuration_file_response = json.dumps(configuration_file)
        return make_response(configuration_file_response, 200)
    except ValueError as Error:
        return make_response(str(Error), 404)
