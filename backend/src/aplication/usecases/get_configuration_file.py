import json
import os

from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "n_files": {"type": "string", "minLength": 1},
        "n_cols": {"type": "array", "items": {"type": "string", "minLength": 1}},
        "cols_types": {"type": "array", "items": {"type": "array", "minItems": 1}},
        "allowed_nulls": {
            "type": "array",
            "items": {"type": "string", "enum": ["0", "1"]},
        },
        "aditional_description": {"type": "string", "minLength": 0},
    },
    # Define los campos requeridos en el archivo JSON
    "required": [
        "name",
        "n_files",
        "n_cols",
        "cols_types",
        "allowed_nulls",
        "aditional_description",
    ],
}


def get_configuration_file(algorithm: str) -> dict or ValueError:
    path = os.path.dirname(os.path.realpath(__file__))
    path = path.rsplit("aplication", 1)[0] + "domain/configuration/"
    json_path = path + algorithm + ".json"
    try:
        with open(json_path, "r") as file:
            data_from_json = json.load(file)
        validate(instance=data_from_json, schema=schema)
        return data_from_json
    except:
        raise ValueError("There is a problem with configuration file.")
