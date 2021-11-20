from flask import redirect, url_for
from flask_app import flask_app

@flask_app.route('/', methods=['GET'])
def routes_root():
  return redirect(url_for('routes_read', uid = ''))
