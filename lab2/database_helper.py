import sqlite3
from flask import Flask
from flask import g
import json

DATABASE = '/lab2/database.db'

app = Flask(__name__)

def find_user(email):
    user = query_db("SELECT * FROM Users WHERE email=?", [email], one=True)
    if user is None:
        return None
    return user

def remove_user(email):
    query = "IF  EXISTS (SELECT * FROM database.Users WHERE email=?) DELETE FROM database.Users WHERE email=?"
    query_db(query, [email], one=True)
    return

def create_post():
    return

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('database.schema', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print "Database initalized"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#def make_dicts(cursor, row):
 #   return dict((cursor.description[idx][0], value)
  #              for idx, value in enumerate(row))


