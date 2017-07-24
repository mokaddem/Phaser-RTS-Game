#!/usr/bin/python3

import configparser
import json
from pprint import pprint
from flask import Flask, render_template, jsonify, request
app = Flask(__name__, static_url_path='/static/')

import MapObjectDefinition
import MapDefinition
from gameLogic import mainGamelogicThread, PlayerRequest

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

the_map = None
all_requests = []
all_updates = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/getMapState/")
def getMapState():
    the_state = the_map.getJsonMapState()
    return the_state
    #return jsonify(the_state)

@app.route("/getGameConfiguration/")
def getGameConfiguration():
    gameConf = {}
    gameConf['width'] = cfg.getint('map', 'width') #x 
    gameConf['height'] = cfg.getint('map', 'height') #y
    gameConf['playerNum'] = cfg.getint('map', 'playerNum')
    return jsonify(gameConf)

@app.route('/baseMapUpdate/', methods = ['POST'])
def baseMapUpdate():
    jsondata = request.get_json()

    return json.dumps(all_updates)

@app.route('/clickCell/', methods = ['POST'])
def clickCell():
    jsondata = request.get_json()
    x = jsondata['x']
    y = jsondata['y']

    ThePlayerRequest = PlayerRequest('unit', 'meleUnit', x, y)
    all_requests.append(ThePlayerRequest)
    #unit = MapObjectDefinition.meleUnit()
    #the_map.placeObject(unit, x, y)

    #to_return = []
    #to_return.append(modif_obj)
    #return json.dumps(to_return)
    
    #modif_obj = the_map.getJsonCell(x, y)
    #all_updates.append(modif_obj)
    return json.dumps({})


def main():
    global the_map
    the_map = MapDefinition.Map(all_updates)

    #mapState1 = the_map.getMapState()
    #core1 = MapObjectDefinition.Core()
    #the_map.placeObject(core1, 2, 10)
    #core2 = MapObjectDefinition.Core()
    #the_map.placeObject(core2, 97, 10)
    #mapState = the_map.getMapState()
    #print(mapState)

    mainGamelogic = mainGamelogicThread("gameLogic", the_map, all_requests, all_updates)
    mainGamelogic.start()


if __name__ == "__main__":
    main()
    #app.run(host='0.0.0.0', port=9000, threaded=True)
    app.run(host='0.0.0.0', port=9000)
