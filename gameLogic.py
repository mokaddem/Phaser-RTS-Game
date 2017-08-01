#!/usr/bin/python3

import configparser
import json
from pprint import pprint
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, send
import threading
import time

import settings as glob
import MapObjectDefinition
import MapDefinition
from utils import ActionEvent, ActionEventManager

cfg = glob.cfg
socketio = SocketIO(message_queue='redis://')


class refreshState():
    def __init__(self, stateType='server'):
        self.nextRefresh = time.time()
        self.refreshRate = cfg.getint('game', stateType+'RefreshRate') #perSec
        self.timeToWaitForRefresh = 1 / float(self.refreshRate)

    def canRefresh(self):
        if self.nextRefresh < time.time():
            self.nextRefresh = time.time() + self.timeToWaitForRefresh
            return True
        else:
            return False

    def getTimeBeforeNextRefresh(self):
        return self.nextRefresh - time.time()


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
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

        self.allUnits = {}
        self.allStructures = []

    def run(self):
        print("Starting main game logic thread", time.ctime(time.time()))
        self.start_main_loop()
        print("Exiting main game logic thread", time.ctime(time.time()))

    def placeCores(self):
        core1 = MapObjectDefinition.Core(glob.the_map, player=1)
        core2 = MapObjectDefinition.Core(glob.the_map, player=2)
        self.allStructures.append(core1)
        self.allStructures.append(core2)

        glob.the_map.placeObject(core1, 1, 4)
        glob.the_map.placeObject(core2, 42, 4)

    def processPlayerRequest(self):
        while len(glob.all_requests) > 0:
            request = glob.all_requests.pop()
            if request.isUnitRequest():
                x = request.x
                y = request.y
                if request.theType == 'meleUnit':
                    unit = MapObjectDefinition.MeleUnit(player=1, posX=x, posY=y)
                    self.allUnits[unit.globalID] = unit
                    glob.the_map.placeObject(unit, x, y)
                    print('MeleUnit created and placed')
                elif request.theType == 'rangedUnit':
                    unit = MapObjectDefinition.RangedUnit(player=1, posX=x, posY=y)
                    self.allUnits[unit.globalID] = unit
                    glob.the_map.placeObject(unit, x, y)

    def executeGameLogic(self):
        #kill all dead unit
        for globalID in glob.actionEventManager.getAndClearKilledUnit():
            self.allUnits.pop(globalID, None)

        #make valid unit behave
        for globalID, unit in self.allUnits.items():
            unit.behave()

    def start_main_loop(self):
        serverState = refreshState()
        clientState = refreshState('client')
        self.placeCores()

        while not glob.startGame:
            time.sleep(0.2)

        print("game started")

        while not glob.gameFinished:
            if serverState.canRefresh():
                if clientState.canRefresh():
                    to_send = glob.actionEventManager.getAllEvents()
                    socketio.emit('baseMapUpdateResp', to_send)
                    glob.actionEventManager.clearAllEvents()

                #process player request
                self.processPlayerRequest()
                #execute main game logic
                self.executeGameLogic()
            else:
               time.sleep(serverState.getTimeBeforeNextRefresh())

