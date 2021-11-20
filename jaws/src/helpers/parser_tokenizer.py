def tokenize(str):
  retval = []
  parsing = []
  tmp = ''

  i = 0
  while i < len(str):
    c = str[i]
    if len(parsing) == 0 and c == '[' and peek(str, i + 1) == '[' and peek(str, i + 2) == '/':
      [retval, tmp] = reset_tmp(retval, tmp)
      retval.append({'type': 'type_stop'})
      parsing.append('type')
      i += 2
    elif len(parsing) == 0 and c == '[' and peek(str, i + 1) == '[':
      [retval, tmp] = reset_tmp(retval, tmp)
      retval.append({'type': 'type_start'})
      parsing.append('type')
      i += 1
    elif is_parsing(parsing, 'type', 'type_parameter_name') and c == '/' and peek(str, i + 1) == ']' and peek(str, i + 2) == ']':
      if parsing[-1] == 'type':
        [retval, tmp] = reset_tmp(retval, tmp.strip().lower(), 'type')
      else:
        [retval, tmp] = reset_tmp(retval, tmp.strip().lower(), 'parameter_name')
        parsing.pop()
      retval.append({'type': 'type_end_quick'})
      parsing.pop()
      i += 2
    elif is_parsing(parsing, 'type', 'type_parameter_name') and c == ']' and peek(str, i + 1) == ']':
      if parsing[-1] == 'type':
        [retval, tmp] = reset_tmp(retval, tmp.strip().lower(), 'type')
      else:
        [retval, tmp] = reset_tmp(retval, tmp.strip().lower(), 'parameter_name')
        parsing.pop()
      retval.append({'type': 'type_end'})
      parsing.pop()
      i += 1
    elif is_parsing(parsing, 'type') and c == ' ':
      [retval, tmp] = reset_tmp(retval, tmp.strip(), 'type')
      parsing.append('type_parameter_name')
    elif is_parsing(parsing, 'type_parameter_name') and c == '=':
      [retval, tmp] = reset_tmp(retval, tmp.strip(), 'parameter_name')
      retval.append({'type': 'eq'})
      parsing[-1] = 'type_parameter_value'
    elif is_parsing(parsing, 'type_parameter_value') and c == '"':
      if retval[-1]['type'] == 'str_symbol':
        [retval, tmp] = reset_tmp(retval, tmp)
        parsing.pop()
      retval.append({'type': 'str_symbol'})
    elif len(parsing) == 0 and c == '\n':
      [retval, tmp] = reset_tmp(retval, tmp)
      retval.append({'type': 'newline'})
    elif c != '\r':
      tmp += c
    i += 1

  [retval, tmp] = reset_tmp(retval, tmp)

  return retval

def peek(str, i):
  if len(str) <= i:
    return None
  return str[i]

def reset_tmp(retval, tmp, type = 'text'):
  if len(tmp) > 0:
    retval.append({
      'type': type,
      'value': tmp,
    })

  return [retval, '']

def is_parsing(l, *args):
  return len(l) > 0 and l[-1] in args
