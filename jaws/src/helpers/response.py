from flask import json as flask_json
from flask_app import flask_app

def json(d, status=200, mimetype='application/json'):
  return flask_app.response_class(response = flask_json.dumps(d), status = status, mimetype = mimetype)
