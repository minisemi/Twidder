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
        return return_message(False, "Sign in failed. No such user.", user)
    else:
        return return_message(True, "Signed in", user)

@app.route('/sign_up', methods=['POST'])
def sign_up():
    email = request.form['email']
    firstName = request.form['firstName']
    familyName = request.form['familyName']
    password = request.form['password']
    gender = request.form['gender']
    city = request.form['city']
    country = request.form['country']
    query = "INSERT INTO Users VALUES (?,?,?,?,?,?,?)"          #Do we need to specify the database?
    database_helper.query_db(query, [email, firstName, familyName, password, gender, city, country], one=True)
    return "lol"

@app.route('/sign_out', methods=['POST'])
def sign_out():
    token = request.form['token']
    queryString = "IF  EXISTS (SELECT * FROM ActiveUsers WHERE token=?) DELETE FROM ActiveUsers WHERE token=?"
    query = database_helper.query_db(queryString, [token], one=True)
    if query is None:
        return return_message(False, "User not found", query)
    else:
        return return_message(True, "Signed out", query)

@app.route('/change_password', methods=['POST'])
def change_password():
    token = request.form['token']
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    if old_password==new_password:
        user = database_helper.check_if_active(token)
    if user=="NotActive":
        return return_message(False, "User not active", user)         #Last parameter left out, insert null if not working
    if database_helper.check_password(old_password, user)==False:
        return return_message(False, "Wrong password", user)
    queryString = "UPDATE Users SET password=? WHERE user=?"
    database_helper.query_db(queryString, [new_password, user], one=True)
    return return_message(True, "Successfully changed password")

@app.route('/get_user_data_by_token', methods =['GET'])
def get_user_data_by_token():
    token = request.headers['token']
    user = database_helper.check_if_active(token)
    if user == "NotActive":
        return return_message(False,"User not active",user)
    else:
        return return_message(True, "Successfully fetched user data", database_helper.find_user(user))

@app.route('/get_user_data_by_email', methods =['GET'])
def get_user_data_by_email():
    token = request.form['token']
    email = request.form['email']
    user = database_helper.check_if_active(token)
    if user == "NotActive":
        return return_message(False, "User not active", user)
    else:
        return return_message(True, "Successfully fetched user data", database_helper.find_user(email))

@app.route('/get_user_messages_by_token', methods =['GET'])
def get_user_messages_by_token():
    token = request.form['token']
    user = database_helper.check_if_active(token)
    if user == "NotActive":
        return return_message(False, "User not active", user)
    else:
        return return_message(True, "Successfully fetched user messages", database_helper.get_posts(user))

@app.route('/get_user_messages_by_email', methods =['GET'])
def get_user_messages_by_email(token, email):
    token = request.form['token']
    email = request.form['email']
    user = database_helper.check_if_active(token)
    if user == "NotActive":
        return return_message(False, "User not active", user)
    else:
        return return_message(True, "Successfully fetched user messages", database_helper.get_posts(email))
    return 0

@app.route('/post_message', methods =['POST'])
def post_message(token, message, email):
    token = request.form['token']
    message = request.form['message']
    email = request.form['email']
    return 0

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
