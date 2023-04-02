import json
from flask import make_response, request
from src.aplication.usecases.process_algorithm_files import process_algorithm_files

def sort_files(files: dict) -> list[dict]:
    return dict(sorted(files.items()))

async def process_files():
    files = request.data.decode('utf-8')
    json_files = json.loads(files)
    sorted_files = sort_files(json_files)
    try:
        processed_files = process_algorithm_files(sorted_files)
        return make_response(processed_files,200)
    except ValueError as Error:
        return make_response(str(Error), 406)
    except Exception as Error:
        return make_response("Something gone wrong with your body request, check it and try again.", 400)
