#!/usr/bin/python3

import configparser
import json
from pprint import pprint
from flask import Flask, render_template, jsonify, request
app = Flask(__name__, static_url_path='/static/')
import threading
import time

import MapObjectDefinition
import MapDefinition

cfg = configparser.ConfigParser()
cfg.read('config.cfg')
refreshRate = cfg.getint('game', 'refreshRate') #perSec
timeToWaitForRefresh = 1 / float(refreshRate)

class PlayerRequest():
    def __init__(self, ObjectType, theType, x=0, y=0):
        self.ObjectType = ObjectType
        self.theType = theType
        self.x = x
        self.y = y

    def isUnitRequest(self):
        if self.ObjectType == 'unit':
            return True
        else:
            return False


class mainGamelogicThread(threading.Thread):
    def __init__(self, name, the_map, all_requests, all_updates):
        threading.Thread.__init__(self)
        self.name = name
        self.the_map = the_map
        self.all_requests = all_requests
        self.all_updates = all_updates

    def run(self):
        print("Starting main game logic thread", time.ctime(time.time()))
        start_main_loop(self, self.name, self.the_map, self.all_requests, self.all_updates)
        print("Exiting main game logic thread", time.ctime(time.time()))

def start_main_loop(thread, threadName, the_map, all_requests, all_updates):
    core1 = MapObjectDefinition.Core()
    the_map.placeObject(core1, 2, 10)
    core2 = MapObjectDefinition.Core()
    the_map.placeObject(core2, 97, 10)

    while True:
        time.sleep(timeToWaitForRefresh)
        #process request
        #execute main game logic
        while len(all_requests) > 0:
            request = all_requests.pop()
            if request.isUnitRequest():
                x = request.x
                y = request.y
                if request.theType == 'meleUnit':
                    unit = MapObjectDefinition.meleUnit()
                    the_map.placeObject(unit, x, y)
                    print('MeleUnit created and placed')
                elif request.theType == 'rangedUnit':
                    unit = MapObjectDefinition.rangedUnit()
                    the_map.placeObject(unit, x, y)

