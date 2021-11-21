from flask import render_template
from flask_app import flask_app
import traceback

def render_error_page(httpcode, title, description = None):
  return render_template(
    'error.html',
    code = httpcode,
    title = title,
    description = description,
  )

def page_not_found():
  return render_error_page(404, 'Not Found')

@flask_app.errorhandler(404)
def errorhandler_404(e):
  return page_not_found()

@flask_app.errorhandler(405)
def errorhandler_405(e):
  return render_error_page(405, 'Method Not Allowed')

@flask_app.errorhandler(Exception)
def exception(e):
  lines = [l[:-1].split('\n') for l in traceback.format_exception(type(e), e, e.__traceback__)]
  lines = ['--> ' + item for sublist in lines for item in sublist]
  print('EXCEPTION:\n' + '\n'.join(lines))
  return render_error_page(500, 'Internal Error', lines)
