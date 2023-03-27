from flask import make_response
def default():
  return make_response("Not Implemented", 501)