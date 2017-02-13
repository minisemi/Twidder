import sqlite3
from flask import Flask
from flask import g


class Database_helper(object):

    pass

    DATABASE = '/lab2/database.db'

    app = Flask(__name__)

    def findUser(self):
        return

    def remove_user(self):
        return

    def create_post(self):
        return

    def init_db(self):
        with Database_helper.app.app_context():
          db = self.get_db()
        with Database_helper.app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
            db.commit()

    def get_db(self):
        db = getattr(self, Flask, '_database', None)
        if db is None:
            db = Flask._database = sqlite3.connect(Database_helper.DATABASE)
            db.row_factory = sqlite3.Row
        return db

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    def query_db(self, query, args=(), one=False):
        cur = self.get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    #def make_dicts(cursor, row):
     #   return dict((cursor.description[idx][0], value)
      #              for idx, value in enumerate(row))

    @app.route('/')
    def index(self):
        cur = self.get_db().cursor()
