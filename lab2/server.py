from flask import Flask
import database_helper


app = Flask(__name__)

@app.route('/')
def hello_world(self):
    return 'Hello World!'

if __name__ == '__main__':
    app.run()

@app.route('/sign_in')
def sign_in(self, email, password):
    user = database_helper.find_user(email)
    return "Signed in"


def sign_up(email, password, firstname, familyname, gender, city, country):
    return 0


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