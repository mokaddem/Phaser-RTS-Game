#!/usr/bin/env/python3

import configparser
import json
from pprint import pprint
import MapObjectDefinition

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

class Map:
    def __init__(self):
        self.height = cfg.getint('map', 'height') #y
        self.width = cfg.getint('map', 'width') #x
        self.playerNum = cfg.getint('map', 'playerNum')

        #Create map tiles
        #self.map = [[0 for y in range(self.height)] for x in range(self.width)]
        self.map = {}
        for x in range(self.width):
            self.map[x] = {}
            for y in range(self.height):
                self.map[x][y] = MapTile(x, y)

    def getMapState(self):
        #state = [[0 for y in range(self.height)] for x in range(self.width)]
        state = {}
        for x in range(self.width):
            state[x] = {}
            for y in range(self.height):
                state[x][y] = self.map[x][y].getTileState()
        return state
    
    def placeObject(self, objectToBePlaced, x, y):
        self.map[x][y].changeTileType(objectToBePlaced)
        

    def __repr__(self):
        return str(self.map)

class MapTile:
    def __init__(self, x, y, playerNum=2):
        self.x = x
        self.y = y
        self.tileType = TileType()
        self.isRevealedForPlayer = [ False for x in range(playerNum) ]

    def __repr__(self):
        return str(self.tileType)

    def getTileState(self):
        return self.tileType

    def changeTileType(self, newObject):
        self.tileType = newObject.texture


class TileType:
    def __init__(self):
        self.isWalkable = True
        self.isUnit = False
        self.isStructure = False
        self.texture = 'blue'

    def __repr__(self):
        return self.texture
        #return json.dumps(self, default=lambda o: o.__dict__)
        #return self.__dict__


def main():
    map = Map()
    mapState1 = map.getMapState()

    core1 = MapObjectDefinition.Core()
    map.placeObject(core1, 2, 10)
    core2 = MapObjectDefinition.Core()
    map.placeObject(core2, 97, 10)

    mapState = map.getMapState()
    print(mapState)

if __name__ == "__main__":
    main()
