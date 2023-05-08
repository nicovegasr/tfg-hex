import json

from flask import make_response, request

from aplication.usecases.get_algorithm_result import get_algorithm_result


def algorithm_performance():
    try:
        files = json.loads(request.get_data())
        result = get_algorithm_result(files)
        return make_response(result, 200)
    except Exception as Error:
        return make_response(str(Error), 500)
