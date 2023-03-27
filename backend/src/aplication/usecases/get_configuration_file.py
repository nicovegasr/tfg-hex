import os
import json

def get_configuration_file(algorithm: str) -> dict or str:
    path = os.path.dirname(os.path.realpath(__file__))
    path = path.rsplit("aplication", 1)[0] + 'domain/configuration/'
    json_path = path + algorithm + '.json'
    data_from_json = ""
    if os.path.exists(json_path):
        with open(json_path, "r") as file:
            data_from_json = json.load(file)
    return data_from_json