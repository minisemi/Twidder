# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask
from flask import g
import json

DATABASE = 'database.db'

app = Flask(__name__)

def find_user(email):
    user = query_db("SELECT email, firstName, familyName, gender, city, country FROM Users WHERE email=?", [email], one=True)
    if user is None:
        return None
    return user

def remove_user(email):
    query = "IF  EXISTS (SELECT * FROM Users WHERE email=?) DELETE FROM Users WHERE email=?"
    query_db(query, [email], one=True)
    if query_db(query, [email], one=True) is None:
        return None
    return "user removed"

def get_posts(email):
    query = "SELECT message FROM Posts WHERE receiver=?"
    return query_db(query, [email])

def create_post():
    return

#Checks is user is active
def check_if_active(token):
    queryString = "SELECT user FROM ActiveUsers WHERE token=?"
    user = query_db(queryString, [token], one=True)
    email = user['user']
    if email is None:
        return "NotActive"
    return email

#Checks if password is correct
def check_password(password, user):
    queryString = "SELECT password FROM Users WHERE user=? AND password=?"
    correctPassword = query_db(queryString, [user, password], one=True)
    if correctPassword is None:
        return False
    return True

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
    #rv = cur.fetchall()
    rv = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    return (rv[0] if rv else None) if one else rv

#def make_dicts(cursor, row):
 #   return dict((cursor.description[idx][0], value)
  #              for idx, value in enumerate(row))


