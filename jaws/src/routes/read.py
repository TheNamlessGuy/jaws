from flask import redirect, url_for, render_template
from flask_app import flask_app

import helpers.db as db
import helpers.parser as parser

@flask_app.route('/read/', defaults={'uid': ''}, methods=['GET'])
@flask_app.route('/read/<path:uid>', methods=['GET'])
def routes_read(uid):
  if uid.endswith('/'):
    return redirect(url_for('routes_read', uid = uid[:-1]))

  data = db.get_page_data(uid)
  if data is None:
    return redirect(url_for('routes_create', uid = uid))

  return render_template(
    'read.html',
    title = data['title'],
    content = parser.parse(data['content'], uid),
  )
