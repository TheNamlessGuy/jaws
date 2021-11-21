from flask import request, render_template
from flask_app import flask_app

import re

import helpers.db as db

RESULT_CONTENT_MAX_LEN = 600
RESULT_CONTENT_MAX_LEN_HALF = RESULT_CONTENT_MAX_LEN // 2

@flask_app.route('/search/', methods=['GET'])
def routes_search():
  queryStr = request.args.get('q')
  if queryStr is None or queryStr == '':
    return render_template(
      'search.html',
      query = queryStr,
      results = [],
      error = 'Query cannot be empty',
    )

  query = queryStr.split(' ')
  results = db.search(query)

  for i in range(len(results)):
    results[i]['title'] = results[i]['title'].replace('<', '&lt;')
    results[i]['title'] = results[i]['title'].replace('>', '&gt;')
    results[i]['content'] = results[i]['content'].replace('<', '&lt;')
    results[i]['content'] = results[i]['content'].replace('>', '&gt;')

  for q in query:
    if q.startswith('-'):
      continue
    pattern = re.compile(q, re.IGNORECASE)

    for i in range(len(results)):
      # Title
      title = results[i]['title']
      matches = [[m.start(), m.end()] for m in re.finditer(pattern, title)]
      matches.reverse()
      for start, end in matches:
        title = title[:start] + '<b>' + title[start:end] + '</b>' + title[end:]

      if 'weight' in results[i]:
        results[i]['weight'] += len(matches)
      else:
        results[i]['weight'] = len(matches)

      results[i]['title'] = title

      # Content
      content = results[i]['content']
      content_len = len(content)
      matches = [[m.start(), m.end()] for m in re.finditer(pattern, content)]
      if len(matches) == 0:
        continue

      if 'weight' in results[i]:
        results[i]['weight'] += len(matches)
      else:
        results[i]['weight'] = len(matches)

      if 'cut' in results[i]:
        start = 0
        end = content_len
      else:
        start = max(0, matches[0][0] - RESULT_CONTENT_MAX_LEN_HALF)
        end = min(content_len, matches[0][1] + RESULT_CONTENT_MAX_LEN_HALF)
        if end - start < RESULT_CONTENT_MAX_LEN:
          end = min(start + RESULT_CONTENT_MAX_LEN, content_len)

        content = content[start:end]
        if start > 0:
          content = '...' + content
          start -= 3
        if end < content_len:
          content += '...'

      matches = [[m[0] - start, m[1] - start] for m in matches if m[0] >= start and m[1] <= end]
      matches.reverse()
      for start_idx, end_idx in matches:
        content = content[:start_idx] + '<b>' + content[start_idx:end_idx] + '</b>' + content[end_idx:]

      results[i]['content'] = content
      results[i]['cut'] = True

  for i in range(len(results)):
    if 'cut' not in results[i] and len(results[i]['content']) > RESULT_CONTENT_MAX_LEN:
      results[i]['content'] = results[i]['content'][:RESULT_CONTENT_MAX_LEN] + '...'

  results = sorted(results, key = lambda x: x['weight'], reverse = True)

  return render_template(
    'search.html',
    query = queryStr,
    results = results,
  )
