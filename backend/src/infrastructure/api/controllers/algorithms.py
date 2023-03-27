import json
from flask import make_response, request
import src.aplication.usecases.get_available_algorithms as available_algorithms_module

async def available_algorithms():
  available_algorithms: list = available_algorithms_module.get_available_algorithms()
  if (available_algorithms):
    available_algorithms_response = json.dumps(available_algorithms)
    return make_response({"Status code": "200", "Payload": available_algorithms_response}, 200)
  return make_response({"Status code": "404", "Message" : "Not algorithm found in server."}, 404)
  