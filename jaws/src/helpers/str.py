from re import sub

def kebab_case(s):
  # https://www.30secondsofcode.org/python/s/kebab
  return '-'.join(
    sub(r'(\s|_|-)+',' ',
    sub(r'[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+',
    lambda mo: ' ' + mo.group(0).lower(), s)).split())
