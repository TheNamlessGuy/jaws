import psycopg2
import psycopg2.extras

import helpers.error_handling as error_handling
import helpers.dotenv as dotenv

###########
# Helpers #
###########
def open_connection():
  env = dotenv.read()
  return psycopg2.connect(dbname=env['JAWS_DB_NAME'], user=env['JAWS_DB_USER'], password=env['JAWS_DB_PASSWORD'], host=env['JAWS_DB_NETWORK_ALIAS'], port=5432)

def default_on_failed_connection(e):
  error_handling.exception(e)
  return None

def use_connection(
      func,
      args = {},
      cursor_factory = None,
      on_failed_connection = default_on_failed_connection,
    ):
  conn = None
  cur = None

  try:
    conn = open_connection()
    if conn is None:
      on_failed_connection()
    cur = conn.cursor(cursor_factory = cursor_factory)

    return func(conn, cur, args)
  except psycopg2.OperationalError as e:
    return on_failed_connection(e)
  finally:
    if cur:
      cur.close()
    if conn:
      conn.close()

def get_title(uid, default = None):
  data = get_page_data(uid, False)
  return data['title'] if data is not None else default

def get_content(uid, default = None):
  data = get_page_data(uid, False)
  return data['content'] if data is not None else default

def get_metadata(uid, default = None):
  data = get_page_data(uid)
  return data['metadata'] if data is not None else default

#################
# Get page data #
#################
def _get_page_data(conn, cur, args):
  cur.execute('SELECT * FROM jaws.pages WHERE uid = %s', (args['uid'],))
  data = cur.fetchone()
  if data is None:
    return None

  if args['get_metadata']:
    return fill_with_metadata(cur, [data])[0]
  return data

def get_page_data(uid, get_metadata = True):
  return use_connection(
    _get_page_data,
    args = {'uid': uid, 'get_metadata': get_metadata},
    cursor_factory = psycopg2.extras.RealDictCursor,
  )

####################
# Create page data #
####################
def _create_page_data(conn, cur, args):
  cur.execute('INSERT INTO jaws.pages (uid, title, content) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING RETURNING uid', (args['uid'], args['title'], args['content']))
  retval = cur.fetchone() # Will be None if the UID already existed

  if retval is not None:
    conn.commit()

  return retval

def create_page_data(uid, title, content):
  return use_connection(
    _create_page_data,
    args = {'uid': uid, 'title': title, 'content': content},
  )

####################
# Update page data #
####################
def _update_page_data(conn, cur, args):
  cur.execute('UPDATE jaws.pages SET title = %s, content = %s WHERE uid = %s RETURNING uid', (args['title'], args['content'], args['uid']))
  retval = cur.fetchone() # Will be None if the UID didn't exist

  if retval is not None:
    conn.commit()

  return retval

def update_page_data(uid, title, content):
  return use_connection(
    _update_page_data,
    args = {'uid': uid, 'title': title, 'content': content},
  )

##################
# Move page data #
##################
def _move_page_data(conn, cur, args):
  cur.execute('SELECT id FROM jaws.pages WHERE uid = %s', (args['new'],))
  if cur.fetchone() is not None:
    return None

  cur.execute('SELECT id FROM jaws.pages WHERE uid = %s', (args['old'],))
  if cur.fetchone() is None:
    return None

  cur.execute('UPDATE jaws.pages SET uid = %s WHERE uid = %s RETURNING uid', (args['new'], args['old']));

  conn.commit()
  return True

def move_page_data(old, new):
  return use_connection(
    _move_page_data,
    args = {'old': old, 'new': new},
  )

####################
# Delete page data #
####################
def _delete_page_data(conn, cur, args):
  cur.execute('SELECT id FROM jaws.pages WHERE uid = %s', (args['uid'],))
  if cur.fetchone() is None:
    return None

  cur.execute('DELETE FROM jaws.pages WHERE uid = %s', (args['uid'],));
  conn.commit()
  return True

def delete_page_data(uid):
  return use_connection(
    _delete_page_data,
    args = {'uid': uid},
  )

#################
# Create tables #
#################
def _create_tables(conn, cur, args):
  cur.execute('CREATE SCHEMA IF NOT EXISTS jaws')

  cur.execute('CREATE TABLE IF NOT EXISTS jaws.pages (id bigserial PRIMARY KEY, uid text NOT NULL UNIQUE, title text NOT NULL, content text NOT NULL)')

  cur.execute('SELECT * FROM pg_type WHERE typname = %s', ('metadata_type',))
  if cur.fetchone() is None:
    cur.execute("""CREATE TYPE metadata_type AS ENUM (
      'tag'
    )""")

  cur.execute("""CREATE TABLE IF NOT EXISTS jaws.metadata (
    page_id int,
    type metadata_type,
    value text,
    CONSTRAINT fk_pages FOREIGN KEY (page_id) REFERENCES jaws.pages(id)
  )""")

  conn.commit()

  if get_page_data(uid = '') is None:
    with open('../example-front-page.txt', 'r') as f:
      content = f.read()
    create_page_data(uid = '', title = 'Example front page', content = content)

def create_tables():
  return use_connection(_create_tables)

##########
# Search #
##########
def _search(conn, cur, args):
  where = ''
  params = []
  for q in args['query']:
    if where != '':
      where += ' AND'

    if q.startswith('-'):
      where += ' title NOT ILIKE %s AND content NOT ILIKE %s'
      q = q[1:]
    else:
      where += ' (title ILIKE %s OR content ILIKE %s)'
    q = '%' + q + '%'
    params.extend([q, q])

  if where == '':
    return []

  cur.execute('SELECT * FROM jaws.pages WHERE' + where, params)
  return fill_with_metadata(cur, cur.fetchall())

def search(query):
  return use_connection(
    _search,
    args = {'query': query},
    cursor_factory = psycopg2.extras.RealDictCursor,
  )

###########
# Helpers #
###########
def fill_with_metadata(cur, entries):
  for entry in entries:
    cur.execute('SELECT * FROM jaws.metadata WHERE page_id = %s', (entry['id'],))
    entry['metadata'] = cur.fetchall()

  return entries

# DEBUG: Remove
def _remove_tables(conn, cur, args):
  cur.execute('DROP SCHEMA IF EXISTS jaws CASCADE')
  conn.commit()

def remove_tables():
  return use_connection(_remove_tables)
