from flask import make_response
def default():
  return make_response({"Status code": "501", "Mensaje": "Not Implemented"}, 501)