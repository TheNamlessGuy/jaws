import logging

from flask_app import flask_app

import helpers.error_handling
import helpers.db as db

import routes.root
import routes.read
import routes.create
import routes.update
import routes.search

import api.get
import api.create
import api.update

# TODO: Remove
import api.debug

log = logging.getLogger('werkzeug')
log.disabled = True
flask_app.logger.disabled = True

if __name__ == '__main__':
  db.create_tables()
  flask_app.run(host='0.0.0.0', port=8000)
