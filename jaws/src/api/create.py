from flask import request
from flask_app import flask_app

import helpers.response as response
import helpers.db as db

@flask_app.route('/_/create/', methods=['POST'])
def api_create():
  uid = request.form.get('uid')
  if uid is None:
    return 'No UID given', 400

  title = request.form.get('title')
  if title is None:
    return 'No title given', 400

  content = request.form.get('content')
  if content is None:
    return 'No content given', 400

  result = db.create_page_data(uid = uid, title = title, content = content)
  if result is None:
    return "UID '{}' already taken".format(uid), 400

  return '', 200
