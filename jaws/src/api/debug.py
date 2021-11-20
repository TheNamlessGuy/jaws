from flask_app import flask_app

import helpers.response as response
import helpers.db as db

@flask_app.route('/_/debug/', methods=['POST'])
def api_debug():
  db.remove_tables()
  return 'Tables removed', 200
