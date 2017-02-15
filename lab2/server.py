from flask import Flask, request
import database_helper
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/sign_in', methods=['POST'])
def sign_in():
    email = request.form['email']
    password = request.form['password']
    user = database_helper.find_user(email)
    #return user + " : " + password
    if user is None:
        return return_message(False, "No such user", user)
    else:
        return return_message(True, "Najs", user)

@app.route('/sign_up', methods=['POST'])
def sign_up():
    query = "INSERT INTO database.Users VALUES (?,?,?,?,?,?,?)"
    return "lol"

@app.route('/sign_out', methods=['POST'])
def sign_out(token):
    return 0

@app.route('/change_password', methods=['POST'])
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

def return_message (success, message, data):
    d = {
        'success': success,
        '"message': message,
        #'data': ['BDFL', 'Developer'],
        'data': data,
    }
    #json_string = '{"success": "Guido", "message":"Rossum", "data":}'
    return json.dumps(d)

if __name__ == '__main__':
    with app.app_context():
        database_helper.init_db()
    app.run(host="localhost", port=5000, threaded=True)
