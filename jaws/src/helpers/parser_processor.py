import helpers.db as db
import helpers.str as Str

def process(tokens, uid):
  nodes = exprs(tokens, 0, {
    'uid': uid,
  })

  if nodes['consumed'] != len(tokens):
    raise Exception('Consumed ' + str(nodes['consumed']) + ', expected ' + str(len(tokens)))

  retval = nodes['node']
  _generate_toc(retval)
  return retval

def exprs(tokens, i, data):
  offset = 0
  nodes = []

  while True:
    node = expr(tokens, i + offset, data)
    if node is None:
      break
    offset += node['consumed']
    nodes.append(node['node'])

  return {'consumed': offset, 'node': nodes}

def expr(tokens, i, data):
  node = text(tokens, i, data)
  if node is not None:
    return node

  node = type(tokens, i, data)
  if node is not None:
    return node

  node = newline(tokens, i, data)
  if node is not None:
    return node

  return None

def newline(tokens, i, data):
  token = _get(tokens, i)
  return {'consumed': 1, 'node': token} if token['type'] == 'newline' else None

def text(tokens, i, data):
  token = _get(tokens, i)
  return {'consumed': 1, 'node': token} if token['type'] == 'text' else None

def type(tokens, i, data):
  node = type_header(tokens, i, data)
  if node is not None:
    return node

  node = type_i(tokens, i, data)
  if node is not None:
    return node

  node = type_b(tokens, i, data)
  if node is not None:
    return node

  node = type_link(tokens, i, data)
  if node is not None:
    return node

  node = type_bullets(tokens, i, data)
  if node is not None:
    return node

  node = type_numbered_list(tokens, i, data)
  if node is not None:
    return node

  node = type_table(tokens, i, data)
  if node is not None:
    return node

  node = type_toc(tokens, i, data)
  if node is not None:
    return node

  node = type_title(tokens, i, data)
  if node is not None:
    return node

  return None

def parameters_type(tokens, i, data):
  offset = 0
  retval = {}

  while True:
    node = parameter_type(tokens, i + offset, data)
    if node is None:
      break
    offset += node['consumed']
    node = node['node']
    retval[node['name']] = node['value']

  return {'consumed': offset, 'node': retval}

def parameter_type(tokens, i, data):
  offset = 0

  name = _get(tokens, i + offset)
  if name is None or name['type'] != 'parameter_name':
    return None
  offset += 1

  if _type(tokens, i + offset) != 'eq':
    return None
  offset += 1

  value = string(tokens, i + offset, data)
  if value is None:
    return None
  offset += value['consumed']

  return {'consumed': offset, 'node': {'name': name['value'], 'value': value['node']['value']}}

def string(tokens, i, data):
  offset = 0

  if _type(tokens, i + offset) != 'str_symbol':
    return None
  offset += 1

  value = _get(tokens, i + offset)
  if value is None:
    return None
  elif value['type'] == 'str_symbol':
    offset += 1
    value = {'type': 'text', 'value': ''}
  elif value['type'] == 'text':
    offset += 1
    if _type(tokens, i + offset) != 'str_symbol':
      return None
    offset += 1
  else:
    return None

  return {'consumed': offset, 'node': value}

# Types
def type_header(tokens, i, data):
  offset = 0

  # If the header is directly preceeded by a newline, skip it. It gets auto-generated by the HTML tag anyway
  offset += _skip_newline(tokens, i + offset, data)

  start = _type_start(tokens, i + offset, data, 'header')
  if start is None:
    return None
  offset += start['consumed']

  offset += _skip_newlines(tokens, i + offset, data)

  value = _get(tokens, i + offset)
  if value['type'] != 'text':
    return None
  offset += 1

  offset += _skip_newlines(tokens, i + offset, data)

  tmp = _type_stop(tokens, i + offset, data, 'header')
  if tmp is None:
    return None
  offset += tmp['consumed']

  # If the header is directly followed by a newline, skip it. It gets auto-generated by the HTML tag anyway
  offset += _skip_newline(tokens, i + offset, data)

  if 'level' not in start['parameters']:
    start['parameters']['level'] = 1
  else:
    start['parameters']['level'] = int(start['parameters']['level'])
  node = {'type': 'header', 'value': value['value']}
  node.update(start['parameters'])
  return {'consumed': offset, 'node': node}

def type_i(tokens, i, data):
  offset = 0

  tmp = _type_start(tokens, i + offset, data, 'i')
  if tmp is None:
    return None
  offset += tmp['consumed']

  values = exprs(tokens, i + offset, data)
  offset += values['consumed']

  tmp = _type_stop(tokens, i + offset, data, 'i')
  if tmp is None:
    return None
  offset += tmp['consumed']

  return {'consumed': offset, 'node': {'type': 'italic', 'value': values['node']}}

def type_b(tokens, i, data):
  offset = 0

  tmp = _type_start(tokens, i + offset, data, 'b')
  if tmp is None:
    return None
  offset += tmp['consumed']

  values = exprs(tokens, i + offset, data)
  offset += values['consumed']

  tmp = _type_stop(tokens, i + offset, data, 'b')
  if tmp is None:
    return None
  offset += tmp['consumed']

  return {'consumed': offset, 'node': {'type': 'bold', 'value': values['node']}}

def type_link(tokens, i, data):
  offset = 0

  start = _type_quick(tokens, i + offset, data, 'link')
  if start is not None:
    offset += start['consumed']
    values = {'node': []}
  else:
    start = _type_start(tokens, i + offset, data, 'link')
    if start is None:
      return None
    offset += start['consumed']

    values = exprs(tokens, i + offset, data)
    offset += values['consumed']

    tmp = _type_stop(tokens, i + offset, data, 'link')
    if tmp is None:
      return None
    offset += tmp['consumed']

  node = {'type': 'link', 'value': values['node']}
  node.update(start['parameters'])

  node['external'] = node['url'].startswith(('http://', 'https://'))
  if node['external']:
    node['exists'] = True
    empty_value = node['url']
  else:
    empty_value = db.get_title(node['url'])
    if empty_value is None:
      node['exists'] = False
      empty_value = node['url']
    else:
      node['exists'] = True

    if not node['url'].startswith('/'):
      node['url'] = '/' + node['url']
    node['url'] = '/read' + node['url']

  if len(node['value']) == 0:
    node['value'].append({'type': 'text', 'value': empty_value})

  return {'consumed': offset, 'node': node}

def type_numbered_list(tokens, i, data):
  offset = 0
  nodes = []

  while True:
    node = type_numbered_list_entry(tokens, i + offset, data)
    if node is None:
      break
    offset += node['consumed']

    if node['level'] == 1 or len(nodes) == 0:
      nodes.append(node['node'])
    else:
      value = node['node']['value']
      value = [{'type': 'numbered_list', 'value': [{'value': value}]}]

      level = node['level'] - 1
      tmp = nodes[-1]['value']
      while level > 1:
        level -= 1
        tmp = tmp[-1]['value'][-1]['value']

      tmp.extend(value)

  if offset == 0:
    return None

  return {'consumed': offset, 'node': {'type': 'numbered_list', 'value': nodes}}

def type_numbered_list_entry(tokens, i, data):
  offset = 0

  tmp = _type_quick(tokens, i + offset, data, ('numbered-entry', '#'))
  if tmp is None:
    return None
  offset += tmp['consumed']

  level = 1
  while True:
    tmp = _type_quick(tokens, i + offset, data, ('numbered-entry', '#'))
    if tmp is None:
      break
    offset += tmp['consumed']
    level += 1

  values = _grab_to_newline(tokens, i + offset, data)
  if values is None:
    values = {'consumed': 0, 'node': []}
  offset += values['consumed']
  values = values['node']

  offset += _skip_newline(tokens, i + offset, data)

  return {'consumed': offset, 'node': {'value': values}, 'level': level}

def type_bullets(tokens, i, data):
  offset = 0
  nodes = []

  while True:
    node = type_bullet(tokens, i + offset, data)
    if node is None:
      break
    offset += node['consumed']

    if node['level'] == 1 or len(nodes) == 0:
      nodes.append(node['node'])
    else:
      value = node['node']['value']
      value = [{'type': 'bullets', 'value': [{'value': value}]}]

      level = node['level'] - 1
      tmp = nodes[-1]['value']
      while level > 1:
        level -= 1
        tmp = tmp[-1]['value'][-1]['value']

      tmp.extend(value)

  if offset == 0:
    return None

  # If the bullet is directly followed by a newline, skip it. <ul> has such a huge margin that it doesn't matter
  offset += _skip_newline(tokens, i + offset, data)

  return {'consumed': offset, 'node': {'type': 'bullets', 'value': nodes}}

def type_bullet(tokens, i, data):
  offset = 0

  tmp = _type_quick(tokens, i + offset, data, ('bullet', '*'))
  if tmp is None:
    return None
  offset += tmp['consumed']

  level = 1
  while True:
    tmp = _type_quick(tokens, i + offset, data, ('bullet', '*'))
    if tmp is None:
      break
    offset += tmp['consumed']
    level += 1

  values = _grab_to_newline(tokens, i + offset, data)
  if values is None:
    values = {'consumed': 0, 'node': []}
  offset += values['consumed']
  values = values['node']

  # If the bullet is directly followed by a newline, skip it. It gets auto-generated by the HTML anyway
  offset += _skip_newline(tokens, i + offset, data)

  return {'consumed': offset, 'node': {'value': values}, 'level': level}

def type_table(tokens, i, data):
  offset = 0

  tmp = _type_start(tokens, i + offset, data, 'table')
  if tmp is None:
    return None
  offset += tmp['consumed']

  offset += _skip_newlines(tokens, i + offset, data)

  header = type_table_header(tokens, i + offset, data)
  if header is None:
    return None
  offset += header['consumed']
  header_cell_count = len(header['node'])

  offset += _skip_newlines(tokens, i + offset, data)

  rows = []
  while True:
    cells = type_table_cells(tokens, i + offset, data, header_cell_count)
    if cells is None:
      break
    offset += cells['consumed']
    rows.append(cells['node'])

  offset += _skip_newlines(tokens, i + offset, data)

  tmp = _type_stop(tokens, i + offset, data, 'table')
  if tmp is None:
    return None
  offset += tmp['consumed']

  # Only skip one at the end - it gets autogenerated by the HTML
  offset += _skip_newline(tokens, i + offset, data)

  return {'consumed': offset, 'node': {'type': 'table', 'header': header['node'], 'rows': rows}}

def type_table_header(tokens, i, data):
  offset = 0

  tmp = _type_start(tokens, i + offset, data, 'table-header')
  if tmp is None:
    return None
  offset += tmp['consumed']

  offset += _skip_newlines(tokens, i + offset, data)

  cells = type_table_cells(tokens, i + offset, data)
  if cells is None:
    return None
  offset += cells['consumed']

  offset += _skip_newlines(tokens, i + offset, data)

  tmp = _type_stop(tokens, i + offset, data, 'table-header')
  if tmp is None:
    return None
  offset += tmp['consumed']

  offset += _skip_newlines(tokens, i + offset, data)

  return {'consumed': offset, 'node': cells['node']}

def type_table_cells(tokens, i, data, max = None):
  offset = 0
  cells = []

  while True:
    node = type_table_cell(tokens, i + offset, data)
    if node is None:
      break
    offset += node['consumed']
    cells.append(node['node'])
    if max is not None and len(cells) == max:
      break

  if offset == 0:
    return None

  return {'consumed': offset, 'node': cells}

def type_table_cell(tokens, i, data):
  offset = 0

  tmp = _type_start(tokens, i + offset, data, ('table-cell', 'tc'))
  if tmp is None:
    return None
  offset += tmp['consumed']

  values = exprs(tokens, i + offset, data)
  offset += values['consumed']

  tmp = _type_stop(tokens, i + offset, data, ('table-cell', 'tc'))
  if tmp is None:
    return None
  offset += tmp['consumed']

  offset += _skip_newlines(tokens, i + offset, data)

  return {'consumed': offset, 'node': values['node']}

def type_toc(tokens, i, data):
  offset = 0

  tmp = _type_quick(tokens, i + offset, data, 'toc')
  if tmp is None:
    return None
  offset += tmp['consumed']

  return {'consumed': offset, 'node': {'type': 'toc'}}

def type_title(tokens, i, data):
  offset = 0

  start = _type_quick(tokens, i + offset, data, 'title')
  if start is None:
    return None
  offset += start['consumed']

  uid = start['parameters']['uid'] if 'uid' in start['parameters'] else data['uid']
  title = db.get_title(uid, default = uid)
  return {'consumed': offset, 'node': {'type': 'text', 'value': title}}

# Helpers
def _get(tokens, i):
  if i < len(tokens):
    return tokens[i]
  return {'type': None, 'value': None}

def _type(tokens, i):
  return _get(tokens, i)['type']

def _skip_newlines(tokens, i, data):
  offset = 0

  while True:
    node = newline(tokens, i + offset, data)
    if node is None:
      break
    offset += node['consumed']

  return offset

def _skip_newline(tokens, i, data):
  node = newline(tokens, i, data)
  if node is None:
    return 0
  return node['consumed']

def _grab_to_newline(tokens, i, data):
  offset = 0
  retval = []

  while True:
    node = expr(tokens, i + offset, data)
    if node is None or node['node']['type'] == 'newline':
      break
    offset += node['consumed']
    retval.append(node['node'])

  if offset == 0:
    return None

  return {'consumed': offset, 'node': retval}

def _type_start(tokens, i, data, type):
  return __type_startstop(tokens, i, data, type, 'type_start')

def _type_stop(tokens, i, data, type):
  return __type_startstop(tokens, i, data, type, 'type_stop')

def _type_quick(tokens, i, data, type):
  return __type_startstop(tokens, i, data, type, 'type_start', 'type_end_quick')

def __type_startstop(tokens, i, data, type, startstop, end = 'type_end'):
  offset = 0

  if not isinstance(type, tuple):
    type = (type,)

  if _type(tokens, i + offset) != startstop:
    return None
  offset += 1

  node = _get(tokens, i + offset)
  if node['type'] != 'type' or node['value'] not in type:
    return None
  offset += 1

  parameters = parameters_type(tokens, i + offset, data)
  if parameters is not None:
    offset += parameters['consumed']

  if _type(tokens, i + offset) != end:
    return None
  offset += 1

  return {'consumed': offset, 'parameters': parameters['node']}

def _generate_toc(nodes):
  headers = []
  toc = None

  for node in nodes:
    if node['type'] == 'toc':
      if toc is not None:
        raise Exception('More than one TOC')
      toc = node
    elif node['type'] == 'header':
      level = node['level']
      anchor = 'anchor-header'

      arr = headers
      while level > 1:
        level -= 1
        arr = arr[-1]
        anchor += '_' + Str.kebab_case(arr['value'])
        arr = arr['children']

      node['anchor'] = anchor + '_' + Str.kebab_case(node['value'])
      node = node.copy()
      node['children'] = []
      arr.append(node)

  if toc is not None:
    toc['data'] = headers
