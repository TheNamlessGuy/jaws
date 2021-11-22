from flask import redirect, url_for, render_template
from flask_app import flask_app

import helpers.db as db

@flask_app.route('/update/', defaults={'uid': ''}, methods=['GET'])
@flask_app.route('/update/<path:uid>', methods=['GET'])
def routes_update(uid):
  data = db.get_page_data(uid)
  if data is None:
    return "UID '{}' not found".format(uid), 400

  return render_template(
    'edit.html',
    create = False,
    title = data['title'],
    content = data['content'],
  )
