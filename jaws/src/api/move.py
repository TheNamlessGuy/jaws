from flask import request
from flask_app import flask_app

import helpers.response as response
import helpers.db as db

@flask_app.route('/_/move/', methods=['POST'])
def api_move():
  oldUID = request.form.get('old')
  if oldUID is None:
    return 'No old UID given', 400

  newUID = request.form.get('new')
  if newUID is None:
    return 'No new UID given', 400

  result = db.move_page_data(old = oldUID, new = newUID)
  if result is None:
    return "UID '{}' already existed".format(newUID), 400

  return '', 200
