from flask import redirect, url_for, render_template
from flask_app import flask_app

import helpers.db as db

@flask_app.route('/create/', defaults={'uid': ''}, methods=['GET'])
@flask_app.route('/create/<path:uid>', methods=['GET'])
def routes_create(uid):
  data = db.get_page_data(uid)
  if data is not None:
    return "UID '{}' already exists".format(uid), 400

  return render_template(
    'edit.html',
    create = True,
    title = uid,
    content = '',
  )
