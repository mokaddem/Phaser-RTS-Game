#!/usr/bin/env/python3

import configparser
import json
from pprint import pprint
from json import JSONEncoder

import settings as glob
import MapObjectDefinition

cfg = glob.cfg

class ActionEvent:
    def __init__(self, action, curObject, coordXY=(0, 0)):
        self.action = action
        self.name = curObject.name
        self.id_num = curObject.id_num
        self.actionNum = curObject.incActionNum()
        self.coordXY = coordXY

    def getUniqID(self):
        return self.name+str(self.id_num)

    def __repr__(self):
        return MyEncoder().encode(self)

class ActionEventManager:
    def __init__(self):
        self.construction_events = {}
        self.move_events = {}
        self.kill_events = {}
        self.IDToKill = []

    def add_construction_event(self, curObject, coordXY):
        actionEvent = ActionEvent('placing', curObject, coordXY)
        uniqID = actionEvent.getUniqID()
        if uniqID in self.construction_events:
            if self.construction_events[uniqID].actionNum < actionEvent.actionNum:
                self.construction_events[uniqID] = actionEvent
        else:
            self.construction_events[uniqID] = actionEvent

    def add_kill_event(self, curObject):
        actionEvent = ActionEvent('kill', curObject)
        uniqID = actionEvent.getUniqID()
        self.kill_events[uniqID] = actionEvent
        self.IDToKill.append(curObject.globalID)

    def add_move_event(self, curObject, coordXY): #FIXME reset position every x seconds OR when other event occur
        actionEvent = ActionEvent('moving', curObject, coordXY)
        uniqID = actionEvent.getUniqID()
        if uniqID in self.move_events:
            if self.move_events[uniqID].actionNum < actionEvent.actionNum:
                self.move_events[uniqID] = actionEvent
        else:
            self.move_events[uniqID] = actionEvent

    def getAndClearKilledUnit(self):
        temp = self.IDToKill
        self.IDToKill = []
        return temp


    def getAllEvents(self):
        listConstructionEvents = []
        for uniqID, event in self.construction_events.items():
            listConstructionEvents.append(event)
        listConstructionEvents.sort(key=lambda x: x.actionNum)

        listMoveEvents = []
        for uniqID, event in self.move_events.items():
            listMoveEvents.append(event)
        listMoveEvents.sort(key=lambda x: x.actionNum)

        listKillEvents = []
        for uniqID, event in self.kill_events.items():
            listKillEvents.append(event)
        listKillEvents.sort(key=lambda x: x.actionNum)

        to_ret = listConstructionEvents + listMoveEvents + listKillEvents
        return MyEncoder().encode(to_ret)

    def clearAllEvents(self):
        self.construction_events = {}
        self.move_events = {}
        self.kill_events = {}
        
    def __repr__(self):
        return MyEncoder().encode(self)


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class Map:
    def __init__(self):
        self.height = cfg.getint('map', 'height') #y
        self.width = cfg.getint('map', 'width') #x
        self.squareSize = cfg.getint('map', 'squareSize')
        self.playerNum = cfg.getint('map', 'playerNum')
        self.playerWidthZone = cfg.getint('map', 'playerWidthZone')

        #Create map tiles
        #self.map = [[0 for y in range(self.height)] for x in range(self.width)]
        self.map = {}
        for x in range(self.width):
            self.map[x] = {}
            for y in range(self.height):
                isPlayerZone = self.isCoordInPlayerZone(x, y)
                self.map[x][y] = MapTile(x, y, isPlayerZone=isPlayerZone)

    def getMapState(self):
        state = {}
        for x in range(self.width):
            state[x] = {}
            for y in range(self.height):
                state[x][y] = self.map[x][y].getTileState()
        return state

    def getJsonCell(self, x, y):
        return MyEncoder().encode(self.map[x][y])

    def getJsonMapState(self):
        state = self.getMapState()
        return MyEncoder().encode(state)

    def isCoordInPlayerZone(self, x, y):
        isPlayerZone = True if (x < self.playerWidthZone or x > self.width - self.playerWidthZone) else False
        return isPlayerZone
    
    def placeObject(self, objectToBePlaced, x, y):
        modif_obj = self.map[x][y].changeTileType(objectToBePlaced)
        #modif_obj = {'action': 'placing', 'name': objectToBePlaced.name, 'id_num': objectToBePlaced.id_num, 'x': x, 'y': y}
        #modif_obj_json = MyEncoder().encode(modif_obj)
        glob.actionEventManager.add_construction_event(objectToBePlaced, (x, y))
        #glob.all_creation_updates.add(modif_obj_json)

    def moveObject(self, objectToMove, deltaX=1, deltaY=0):
        startX = objectToMove.posX
        startY = objectToMove.posY
        emptyObject = MapTile(startX, startY, isPlayerZone=self.isCoordInPlayerZone(startX, startY))
        modif_emptyObj = self.map[startX][startY].changeTileType(emptyObject.tileType)
        modif_emptyObj_json = MyEncoder().encode(modif_emptyObj)
        #glob.all_updates.append(modif_emptyObj_json)

        endX = startX + deltaX
        endY = startY + deltaY
        print(self.width)
        if endX >= self.width-1 or endY >= self.height-1:
            print('moveOutOfBound')
            glob.actionEventManager.add_kill_event(objectToMove)
        self.map[endX][endY].changeTileType(objectToMove)
        glob.actionEventManager.add_move_event(objectToMove, (endX, endY))
        #modif_obj_json = MyEncoder().encode(modif_obj)
        #glob.all_updates.add(action)

        
    def __repr__(self):
        return MyEncoder().encode(self.map)
        #return json.dumps(self.map)


class MapTile:
    def __init__(self, x, y, playerNum=2, isPlayerZone=False):
        self.x = x
        self.y = y
        self.isPlayerZone = isPlayerZone
        self.tileType = TileType(isPlayerZone)
        self.isRevealedForPlayer = [ False for x in range(playerNum) ]

    def __repr__(self):
        return MyEncoder().encode(self.tileType)
        #return json.dumps(self.tileType)

    def getTileState(self):
        return { 'tileType': self.tileType, 'x': self.x, 'y': self.y }

    def changeTileType(self, newObject):
        self.tileType.tileColor = newObject.tileColor
        self.tileType.isUnit = newObject.isUnit
        self.tileType.isStructure = newObject.isStructure
        self.tileType.isWalkable = newObject.isWalkable
        return self


class TileType:
    def __init__(self, isPlayerZone=False):
        self.isWalkable = True
        self.isUnit = False
        self.isStructure = False
        if isPlayerZone:
            self.tileColor = 'playerzone'
        else:
            self.tileColor = 'warzone'

    def __repr__(self):
        return MyEncoder().encode(self.tileColor)
        #return json.dumps(self.tileColor)

