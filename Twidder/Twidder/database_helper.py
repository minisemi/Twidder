# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask
from flask import g

import json
import time

DATABASE = 'database.db'

app = Flask(__name__)

def find_user(email):
    user = query_db("SELECT email, firstName, familyName, gender, city, country FROM Users WHERE email=?", [email], one=True)
    if user is None:
        return None
    return user

def update_page_views(user):
    query = "UPDATE Users SET pageViews = pageViews + 1 WHERE email = ?"
    query_db(query, [user], one=True)

def get_posts_count(user):
    query = "SELECT COUNT(message) FROM Posts WHERE receiver=?"
    return query_db(query, [user], one=True)

def get_post_to_others_count(user):
    query = "SELECT COUNT(message) FROM Posts WHERE sender=? AND receiver!=?"
    return query_db(query, [user, user], one=True)


def get_views_count(user):
    query = "SELECT pageViews FROM Users WHERE email=?"
    return query_db(query, [user], one=True)

def remove_active_user(user):
    query = "DELETE FROM ActiveUsers WHERE user=?"
    query_db(query, [user], one=True)


def add_user(email, firstName, familyName, password, gender, city, country):
    query = "INSERT INTO Users VALUES (?,?,?,?,?,?,?,?)"          #Do we need to specify the database?
    query_db(query, [email, firstName, familyName, password, gender, city, country, 0], one=True)


def remove_user(email):
    query = "IF  EXISTS (SELECT * FROM Users WHERE email=?) DELETE FROM Users WHERE email=?"
    query_db(query, [email], one=True)
    if query_db(query, [email], one=True) is None:
        return None
    return "user removed"


def get_posts(email):
    query = "SELECT message, sender FROM Posts WHERE receiver=?"
    return query_db(query, [email])


def create_post(sender, receiver, message):
    query = "INSERT INTO Posts VALUES (?,?,?,?)"
    query_db(query, [receiver, sender, message, time.time()], one=True)


#Checks is user is active
def check_if_active(token):
    queryString = "SELECT user FROM ActiveUsers WHERE token=?"
    user = query_db(queryString, [token], one=True)
    if user is None:
        return "NotActive"
    email = user['user']
    return email

def check_if_active_email(email):
    query = "SELECT user FROM ActiveUsers WHERE user=?"
    user = query_db(query, [email], one=True)
    if user is None:
        return "NotActive"
    email = user['user']
    return email

def add_active_user(email, token):
    if check_if_active_email(email) is not "NotActive":
        remove_active_user(email)
    query = "INSERT INTO ActiveUsers VALUES (?, ?)"
    query_db(query, [email, token], one=True)

#Checks if password is correct
def check_password(password, email):
    query = "SELECT password FROM Users WHERE email=? AND password=?"
    correct_password = query_db(query, [email, password], one=True)
    if correct_password is None:
        return False
    return True

def update_password(password, user):
    query = "UPDATE Users SET password=? WHERE email=?"
    query_db(query, [password, user], one=True)

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
    db = get_db()
    cur = db.execute(query, args)
    #rv = cur.fetchall()
    rv = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
    db.commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#def make_dicts(cursor, row):
 #   return dict((cursor.description[idx][0], value)
  #              for idx, value in enumerate(row))


