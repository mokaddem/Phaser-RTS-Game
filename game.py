#!/usr/bin/python3

import json
import time
from pprint import pprint
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, send

import settings as glob
import MapObjectDefinition
import MapDefinition
from gameLogic import mainGamelogicThread, PlayerRequest

import eventlet
eventlet.monkey_patch()

app = Flask(__name__, static_url_path='/static/')
glob.app = app
#socketio = SocketIO(app)
socketio = SocketIO(app, message_queue='redis://')
glob.socketio = socketio

cfg = glob.cfg

all_requests = []
glob.all_requests = all_requests
all_updates = set()
glob.allupdates = all_updates
all_creation_updates = set()
glob.all_creation_updates = all_creation_updates


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

#@socketio.on('baseMapUpdate')
#def handle_baseMapUpdate(receivedJson):
#    global all_updates

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
    glob.startGame = True


def main():
    glob.the_map = MapDefinition.Map()
    glob.actionEventManager = MapDefinition.ActionEventManager()

    mainGamelogic = mainGamelogicThread("gameLogic")
    mainGamelogic.start()


if __name__ == "__main__":
    main()
    #app.run(host='0.0.0.0', port=9000, threaded=True)
    #app.run(host='0.0.0.0', port=9000)
    socketio.run(app, host='0.0.0.0', port=9000)
