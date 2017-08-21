#!/usr/bin/env python

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
users = {'user1': {'password': 'pass'}, 'user2': {'password': 'pass'}}

cfg = glob.cfg

all_requests = []
glob.all_requests = all_requests


@flask_login.login_required
@app.route('/')
def index():
    if flask_login.current_user.is_authenticated:
        return render_template('index.html')
    else:
        return flask.redirect(flask.url_for('login'))


@flask_login.login_required
@app.route("/getMapState/")
def getMapState():
    the_state = glob.the_map.getJsonMapState()
    return the_state
    #return jsonify(the_state)

@flask_login.login_required
@app.route("/getGameConfiguration/")
def getGameConfiguration():
    curUser = flask_login.current_user
    gameConf = {}
    gameConf['width'] = cfg.getint('map', 'width') #x 
    gameConf['height'] = cfg.getint('map', 'height') #y
    gameConf['squareSize'] = cfg.getint('map', 'squareSize') #y
    gameConf['playerNumber'] = cfg.getint('map', 'playerNumber')
    gameConf['playerID'] = curUser.playerID
    return jsonify(gameConf)

@flask_login.login_required
@socketio.on('cell')
def handle_cell(receivedJson):
    curUser = flask_login.current_user
    print('received json: ' + str(receivedJson))
    jsondata = receivedJson['data']
    x = jsondata["x"]
    y = jsondata['y']

    import random
    unitType = 'meleUnit' if random.random() > 0.5 else 'rangedUnit'
    ThePlayerRequest = PlayerRequest('unit', unitType, curUser.playerID, x, y)
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
    curUser = flask_login.current_user
    glob.players[curUser.playerID].setReady()

    for player in glob.players:
        if not player.isReady():
            return 
    glob.startGame = True

@glob.login_manager.user_loader
def user_loader(username):
    try:
        if username not in users:
            return
        user = User()
        user.id = username
        user.loadUser(glob.usernameToPlayer[username])
        return user
    except:
        return

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'></input>
                <input type='password' name='password' id='password' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    username = request.form['username']
    try:
        if request.form['password'] == users[username]['password']:
            user = User()

            #Attribute this user to a player object
            player_to_be_attributed = None
            for player in glob.players:
                if not player.isAttributed():
                    player_to_be_attributed = player
                    break
            player_to_be_attributed.attribute()

            user.id = username
            glob.usernameToPlayer[username] = player_to_be_attributed
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('index'))

    except KeyError:
        return flask.redirect(flask.url_for('unprotected'))

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: {}, player number: {}'.format(flask_login.current_user.id, flask_login.current_user.playerID)

@app.route('/unprotected')
def unprotected():
    return '<p>not logged in</p>' 

def main():
    glob.players = [Player(i) for i in range(cfg.getint('map' ,'playerNumber'))]
    glob.the_map = MapDefinition.Map()
    glob.actionEventManager = MapDefinition.ActionEventManager()

    mainGamelogic = mainGamelogicThread("gameLogic")
    mainGamelogic.start()


if __name__ == "__main__":
    main()
    #app.run(host='0.0.0.0', port=9000, threaded=True)
    #app.run(host='0.0.0.0', port=9000)
    socketio.run(app, host='0.0.0.0', port=9000)
