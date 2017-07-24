#!/usr/bin/env/python3

import configparser
import json
from pprint import pprint
from flask import Flask, render_template, jsonify
app = Flask(__name__, static_url_path='/static/')

import MapObjectDefinition
import MapDefinition

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

the_map = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/getMapState/")
def getMapState():
    the_state = the_map.getJsonMapState()
    pprint(the_state)
    return the_state
    #return jsonify(the_state)

@app.route("/getGameConfiguration/")
def getGameConfiguration():
    gameConf = {}
    gameConf['width'] = cfg.getint('map', 'width') #x 
    gameConf['height'] = cfg.getint('map', 'height') #y
    gameConf['playerNum'] = cfg.getint('map', 'playerNum')
    return jsonify(gameConf)


def main():
    global the_map
    the_map = MapDefinition.Map()
    mapState1 = the_map.getMapState()

    core1 = MapObjectDefinition.Core()
    the_map.placeObject(core1, 2, 10)
    core2 = MapObjectDefinition.Core()
    the_map.placeObject(core2, 97, 10)

    mapState = the_map.getMapState()
    #print(mapState)

if __name__ == "__main__":
    main()
    app.run(host='0.0.0.0', port=9000, threaded=True)
