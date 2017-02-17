# -*- coding: utf-8 -*-
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
        return return_message(False, "Sign in failed. No such user.", None)
    if database_helper.check_password(password, user):
        return return_message(True, "Signed in", None)
    return return_message(False, "Wrong password", None)

@app.route('/sign_up', methods=['POST'])
def sign_up():
    email = request.form['email']
    firstName = request.form['firstName']
    familyName = request.form['familyName']
    password = request.form['password']
    gender = request.form['gender']
    city = request.form['city']
    country = request.form['country']
    user = database_helper.find_user(email)
    if user is not None:
        return return_message(False, "User already exists", None)

    database_helper.sign_up_user(email, firstName, familyName, password, gender, city, country)
    return return_message(True, "Signed up", user)

@app.route('/sign_out', methods=['POST'])
def sign_out():
    token = request.form['token']
    user = database_helper.check_if_active(token)
    if user is None:
        return return_message(False, "User not found", None)

    database_helper.sign_out_user(user)
    return return_message(True, "Signed out", user)

@app.route('/change_password', methods=['POST'])
def change_password():
    token = request.form['token']
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    user = database_helper.check_if_active(token)
    if user=="NotActive":
        return return_message(False, "User not active", None)         #Last parameter left out, insert null if not working
    if database_helper.check_password(old_password, user)==False:
        return return_message(False, "Wrong password", user)
    database_helper.update_password(new_password, user)
    return return_message(True, "Successfully changed password")

@app.route('/get_user_data_by_token', methods =['GET'])
def get_user_data_by_token():
    token = request.headers['token']
    user = database_helper.check_if_active(token)
    if user == "NotActive":
        return return_message(False,"User not active",None)
    else:
        return return_message(True, "Successfully fetched user data", database_helper.find_user(user))

@app.route('/get_user_data_by_email', methods =['GET'])
def get_user_data_by_email():
    token = request.form['token']
    email = request.form['email']
    user = database_helper.check_if_active(token)
    if user == "NotActive":
        return return_message(False, "User not active", None)
    else:
        return return_message(True, "Successfully fetched user data", database_helper.find_user(email))

@app.route('/get_user_messages_by_token', methods =['GET'])
def get_user_messages_by_token():
    token = request.form['token']
    user = database_helper.check_if_active(token)
    if user == "NotActive":
        return return_message(False, "User not active", None)
    else:
        return return_message(True, "Successfully fetched user messages", database_helper.get_posts(user))

@app.route('/get_user_messages_by_email', methods =['GET'])
def get_user_messages_by_email(token, email):
    token = request.form['token']
    email = request.form['email']
    user = database_helper.check_if_active(token)
    if user == "NotActive":
        return return_message(False, "User not active", None)
    else:
        return return_message(True, "Successfully fetched user messages", database_helper.get_posts(email))

@app.route('/post_message', methods =['POST'])
def post_message(token, message, email):
    token = request.form['token']
    message = request.form['message']
    email = request.form['email']
    user = database_helper.check_if_active(token)
    if user=="NotActive":
        return return_message(False, "User not active", None)
    receiver = database_helper.find_user(email)
    if receiver is None:
        return return_message(False, "ReceiverNotFound", None)

    database_helper.create_post()
    return return_message(True, "MessagePosted", user)

def return_message (success, message, data):
    d = {
        'success': success,
        'message': message,
        #'data': ['BDFL', 'Developer'],
        'data': data
    }
    #json_string = '{"success": "Guido", "message":"Rossum", "data":}'
    return json.dumps(d)

if __name__ == '__main__':
    with app.app_context():
        database_helper.init_db()
    app.run(host="localhost", port=5000, threaded=True)
