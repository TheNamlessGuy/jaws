from flask import request
from flask_app import flask_app

import helpers.response as response
import helpers.db as db

@flask_app.route('/_/delete/', methods=['POST'])
def api_delete():
  uid = request.form.get('uid')
  if uid is None:
    return 'No UID given', 400

  result = db.delete_page_data(uid = uid)
  if result is None:
    return "UID '{}' doesn't exist".format(uid), 400

  return '', 200
