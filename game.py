#!/usr/bin/python3

import json
import time
from pprint import pprint
import flask
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, send
import flask_login

import settings as glob
import MapObjectDefinition
import MapDefinition
from utils import ActionEvent, ActionEventManager, Player, User
from gameLogic import mainGamelogicThread, PlayerRequest

import eventlet
eventlet.monkey_patch()

app = Flask(__name__, static_url_path='/static/')
app.secret_key = 'super secret string'  # Change this!
glob.app = app
socketio = SocketIO(app, message_queue='redis://')
glob.socketio = socketio
glob.login_manager = flask_login.LoginManager()
glob.login_manager.init_app(app)
users = {'foo@bar.tld': {'pw': 'secret'}}

cfg = glob.cfg

all_requests = []
glob.all_requests = all_requests


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/getMapState/")
def getMapState():
    the_state = glob.the_map.getJsonMapState()
    return the_state
    #return jsonify(the_state)

@app.route("/getGameConfiguration/")
def getGameConfiguration():
    gameConf = {}
    gameConf['width'] = cfg.getint('map', 'width') #x 
    gameConf['height'] = cfg.getint('map', 'height') #y
    gameConf['squareSize'] = cfg.getint('map', 'squareSize') #y
    gameConf['playerNum'] = cfg.getint('map', 'playerNum')
    return jsonify(gameConf)

@socketio.on('cell')
def handle_cell(receivedJson):
    print('received json: ' + str(receivedJson))
    jsondata = receivedJson['data']
    x = jsondata["x"]
    y = jsondata['y']

    import random
    unitType = 'meleUnit' if random.random() > 0.5 else 'rangedUnit'
    ThePlayerRequest = PlayerRequest('unit', unitType, x, y)
    #ThePlayerRequest = PlayerRequest('unit', 'ranged#Unit', x, y)
    glob.all_requests.append(ThePlayerRequest)


@socketio.on('disconnect')
def test_disconnect():
    print('/!\ CLIENT DISCONNECTED /!\ ')

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('gameReady')
def gameReady(receivedJson):
    glob.players[0].setReady()
    glob.players[1].setReady()

    for player in glob.players:
        if not player.isReady():
            return 
    glob.startGame = True

@glob.login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@glob.login_manager.request_loader
def request_loader(request):
    email = request.form.get('foo@bar.tld')
    if email not in users:
        return
    user = User()
    user.id = email
    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = 'secret' == users[email]['pw']
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = request.form['email']
    try:
        if request.form['pw'] == users[email]['pw']:
            user = User()
            user.id = email
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('protected'))
    except KeyError:
        return flask.redirect(flask.url_for('unprotected'))

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/unprotected')
def unprotected():
    return '<p>not logged in</p>' 

def main():
    glob.players = [Player(i) for i in range(cfg.getint('map' ,'playerNum'))]
    glob.the_map = MapDefinition.Map()
    glob.actionEventManager = MapDefinition.ActionEventManager()

    mainGamelogic = mainGamelogicThread("gameLogic")
    mainGamelogic.start()


if __name__ == "__main__":
    main()
    #app.run(host='0.0.0.0', port=9000, threaded=True)
    #app.run(host='0.0.0.0', port=9000)
    socketio.run(app, host='0.0.0.0', port=9000)
