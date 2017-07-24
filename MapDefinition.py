#!/usr/bin/env/python3

import configparser
import json
from pprint import pprint
from json import JSONEncoder
import MapObjectDefinition

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
class Map:
    def __init__(self):
        self.height = cfg.getint('map', 'height') #y
        self.width = cfg.getint('map', 'width') #x
        self.playerNum = cfg.getint('map', 'playerNum')
        self.playerWidthZone = cfg.getint('map', 'playerWidthZone')

        #Create map tiles
        #self.map = [[0 for y in range(self.height)] for x in range(self.width)]
        self.map = {}
        for x in range(self.width):
            self.map[x] = {}
            for y in range(self.height):
                isPlayerZone = True if (x < self.playerWidthZone or x > self.width - self.playerWidthZone) else False
                self.map[x][y] = MapTile(x, y, isPlayerZone=isPlayerZone)

    def getMapState(self):
        state = {}
        for x in range(self.width):
            state[x] = {}
            for y in range(self.height):
                state[x][y] = self.map[x][y].getTileState()
        return state

    def getJsonMapState(self):
        state = self.getMapState()
        return MyEncoder().encode(state)
    
    def placeObject(self, objectToBePlaced, x, y):
        self.map[x][y].changeTileType(objectToBePlaced)
        

    def __repr__(self):
        return json.dumps(self.map)


class MapTile:
    def __init__(self, x, y, playerNum=2, isPlayerZone=False):
        self.x = x
        self.y = y
        self.isPlayerZone = isPlayerZone
        self.tileType = TileType(isPlayerZone)
        self.isRevealedForPlayer = [ False for x in range(playerNum) ]

    def __repr__(self):
        return json.dumps(self.tileType)

    def getTileState(self):
        return { 'tileState': self.tileType, 'x': self.x, 'y': self.y }

    def changeTileType(self, newObject):
        self.tileType.tileColor = newObject.tileColor
        self.tileType.isUnit = newObject.isUnit
        self.tileType.isStructure = newObject.isStructure
        self.tileType.isWalkable = newObject.isWalkable


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
        return json.dumps(self.tileColor)
