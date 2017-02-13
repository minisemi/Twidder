from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()


def sign_in(email, password):

    return 0


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