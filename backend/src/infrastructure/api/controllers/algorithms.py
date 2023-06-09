import json

from flask import make_response

import aplication.usecases.get_available_algorithms as available_algorithms_module


def available_algorithms():
    try:
        available_algorithms: list = (
            available_algorithms_module.get_available_algorithms()
        )
        if not available_algorithms:
            return make_response("Not algorithm found in server.", 404)
        available_algorithms_response = json.dumps(available_algorithms)
        return make_response(available_algorithms_response, 200)
    except ValueError as Error:
        return make_response(str(Error), 501)
