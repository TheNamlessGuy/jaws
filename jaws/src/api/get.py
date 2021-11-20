from flask_app import flask_app

import helpers.response as response
import helpers.db as db
import helpers.parser_tokenizer as tokenizer
import helpers.parser_processor as processor

@flask_app.route('/_/get/', defaults={'uid': ''}, methods=['GET', 'POST'])
@flask_app.route('/_/get/<path:uid>', methods=['GET', 'POST'])
def api_get(uid):
  data = db.get_page_data(uid)
  if data is None:
    return "UID '{}' not found".format(uid), 400

  try:
    tokens = tokenizer.tokenize(data['content'])
  except:
    tokens = None

  try:
    nodes = processor.process(tokens)
  except:
    nodes = None

  return response.json({
    'item': data,
    'tokens': tokens,
    'nodes': nodes
  })
