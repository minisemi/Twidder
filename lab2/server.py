from flask import Flask, request
import database_helper

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/sign_in', methods=['POST'])
def sign_in():
    user = request.form['email']
    password = request.form['password']
    # user = database_helper.find_user(email)
    return user + " : " + password

@app.route('/sign_in', methods=['POST'])
def sign_up(email, password, firstname, familyname, gender, city, country):
    return 0

@app.route('/sign_in', methods=['POST'])
def sign_out(token):
    return 0

@app.route('/sign_in', methods=['POST'])
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

if __name__ == '__main__':
    app.run(host="localhost", port=5000, threaded=True)