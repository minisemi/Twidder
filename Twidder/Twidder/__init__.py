# -*- coding: utf-8 -*-
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket import WebSocketError
from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer
from flask_sockets import Sockets
import database_helper
import json
import re
import uuid

app = Flask(__name__, static_url_path='')
sockets = Sockets(app)
socket_storage = {}

@sockets.route('/echo')
def echo_socket(ws):
    while True:
        try:
            message = ws.receive()
            email = database_helper.check_if_active(message)
        except WebSocketError:
            socket_storage.pop(email)
        if socket_storage.get(email):
            try:
                socket_storage[email].send(return_message(True, 'logout', None))
                socket_storage.pop(email)

            except IOError:
                print(IOError)
        socket_storage[email] = ws
        try:
            socket_storage[email].send(return_message(True, 'updateChart', {'chartType': 'posts', 'chartValue': database_helper.get_posts_count(email)}))
            socket_storage[email].send(return_message(True, 'updateChart', {'chartType': 'visits','chartValue': database_helper.get_views_count(email)}))
        except WebSocketError:
            socket_storage.pop(email)

        if bool(socket_storage):
            for mail, socket in socket_storage.items():
                try:
                    socket.send(return_message(True, 'updateChart', {'chartType': 'members', 'chartValue': len(socket_storage)}))
                except WebSocketError:
                    socket_storage.pop(mail)


@app.route('/Home')
def home():
    return root()

@app.route('/Browse')
def browse():
    return root()

@app.route('/Account')
def account():
    return root()

#@app.route('/', defaults={'path': ''})
@app.route('/')#<path:path>')
def root():
    return app.send_static_file('client.html')
    #return render_template('client.html')

@app.route('/sign_in', methods=['POST'])
def sign_in():
    email = request.form['email']
    password = request.form['password']
    user = database_helper.find_user(email)
    if user is None:
        return return_message(False, "Sign in failed. No such user.", None)
    if database_helper.check_password(password, email):
        token = str(uuid.uuid4().hex)
        database_helper.add_active_user(email, token)
        for email, socket in socket_storage.items():
            #print(socket_storage)
            socket.send(return_message(True, 'updateChart', {'chartType': 'members', 'chartValue': len(socket_storage)}))
        return return_message(True, "Signed in", token)
    return return_message(False, "Wrong password", None)

@app.route('/sign_up', methods=['POST'])#/api/sign...
def sign_up():
    email = request.form['email']
    firstName = request.form['firstName']
    familyName = request.form['familyName']
    password = request.form['password']
    gender = request.form['gender']
    city = request.form['city']
    country = request.form['country']

    if len(email)*len(firstName)*len(familyName)*len(password)*len(gender)*len(city)*len(country)==0:
        return return_message(False, "Empty field(s)", None)

    if gender != "Male" and gender!="Female" and gender!="Other":
        return return_message(False, "Invalid gender", None)

    user = database_helper.find_user(email)
    if user is not None:
        return return_message(False, "User already exists", None)
    regex_pattern = re.compile(".+@.+") #googla html5's regex
    if regex_pattern.match(email) is None:
        return return_message(False, "Invalid email address", email)
    if len(password) < 5:
        return return_message(False, "Password too short", None)
    database_helper.add_user(email, firstName, familyName, password, gender, city, country)
    return return_message(True, "Signed up", None)

@app.route('/sign_out', methods=['POST'])
def sign_out():
    token = request.headers['token']
    user = database_helper.check_if_active(token)
    if user is "NotActive":
        return return_message(False, "User not found", None)
    database_helper.remove_active_user(user)
    socket_storage.pop(user)
    if bool(socket_storage):
        for mail, socket in socket_storage.items():
            try:
                socket.send(
                    return_message(True, 'updateChart', {'chartType': 'members', 'chartValue': len(socket_storage)}))
            except WebSocketError:
                socket_storage.pop(mail)
    return return_message(True, "Signed out", None)

@app.route('/change_password', methods=['POST'])#put token in header instead
def change_password():
    token = request.headers['token']
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    user = database_helper.check_if_active(token)
    if user is "NotActive":
        return return_message(False, "User not active", None)
    if database_helper.check_password(old_password, user) is False:
        return return_message(False, "Wrong password", user)
    if len(new_password) < 5 or new_password == old_password:
        return return_message(False, "Invalid new password", None)
            #Last parameter left out, insert null if not working

    database_helper.update_password(new_password, user)
    return return_message(True, "Successfully changed password", None)

@app.route('/get_user_data_by_token', methods =['GET'])
def get_user_data_by_token():
    token = request.headers['token']
    user = database_helper.check_if_active(token)
    if user is "NotActive":
        return return_message(False,"User not active",None)
    else:
        return return_message(True, "Successfully fetched user data", database_helper.find_user(user))

@app.route('/get_user_data_by_email', methods =['GET'])
def get_user_data_by_email():#add param here
    token = request.headers['token']
    email = request.args['email']
    user = database_helper.check_if_active(token)
    if user is "NotActive":
        return return_message(False, "User not active", None)
    user = database_helper.find_user(email)
    if user is None:
        return return_message(False, "No such user", user)

    database_helper.update_page_views(email)
    active_user = database_helper.check_if_active_email(email)
    if active_user != "NotActive":
        try:
            socket_storage[email].send(return_message(True, 'updateChart', {'chartType': 'visits', 'chartValue': database_helper.get_views_count(email)}))
        except WebSocketError:
            socket_storage.pop(email)
    return return_message(True, "Successfully fetched user data", user)

@app.route('/get_user_messages_by_token', methods =['GET'])
def get_user_messages_by_token():
    token = request.headers['token']
    user = database_helper.check_if_active(token)
    if user is "NotActive":
        return return_message(False, "User not active", None)
    else:
        return return_message(True, "Successfully fetched user messages", database_helper.get_posts(user))

@app.route('/get_user_messages_by_email', methods =['GET'])
def get_user_messages_by_email():
    token = request.headers['token']
    email = request.args['email']

    user = database_helper.check_if_active(token)

    if user is "NotActive":
        return return_message(False, "User not active", None)
    user = database_helper.find_user(email)
    if user is None:
        return return_message(False, "No such user", user)
    posts = database_helper.get_posts(email)
    if not posts:
        return return_message(False, "No user messages", None)
    else:
        return return_message(True, "Successfully fetched user messages", database_helper.get_posts(email))

@app.route('/post_message', methods =['POST'])
def post_message():
    token = request.headers['token']
    message = request.form['message']
    sender = request.form['sender']
    email = request.form['email']
    user = database_helper.check_if_active(token)
    if user is "NotActive":
        return return_message(False, "User not active", None)
    receiver = database_helper.find_user(email)
    if receiver is None:
        return return_message(False, "ReceiverNotFound", None)

    database_helper.create_post(sender, email, message)
    active_user = database_helper.check_if_active_email(email)
    if active_user != "NotActive":
        try:
            socket_storage[email].send(return_message(True, 'updateChart', {'chartType': 'posts', 'chartValue': database_helper.get_posts_count(email)}))
        except WebSocketError:
            socket_storage.pop(email)
    return return_message(True, "MessagePosted", None)

def return_message (success, message, data):
    d = {
        'success': success,
        'message': message,
        'data': data
    }
    return json.dumps(d)

if __name__ == '__main__':

    with app.app_context():
        database_helper.init_db()
    http_server = WSGIServer(('', 7000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    #app.run(host="localhost", port=5000, threaded=True)

