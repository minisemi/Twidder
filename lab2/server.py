from flask import Flask
from lab2.database_helper import Database_helper


app = Flask(__name__)

@app.route('/')
def hello_world(self):
    self.db = Database_helper()
    return 'Hello World!'

if __name__ == '__main__':
    app.run()


def sign_in(email, password):

    return 0


def sign_up(email, password, firstname, familyname, gender, city, country):
    query = "INSERT INTO database.Users VALUES (?,?,?,?,?,?,?)"


    return


def sign_out(token):
    return 0


def change_password(token, old_password, new_password):
    return 0


def get_user_data_by_token(token):
    return 0

def get_user_data_by_email(token, email):

    return 0


def get_user_messages_by_token(token):

    return 0


def get_user_messages_by_email(token, email):
    return 0


def post_message(token, message, email):
    return 0