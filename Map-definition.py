#!/usr/bin/python3

import configparser
import json
from pprint import pprint

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

class Map:
    def __init__(self):
        self.height = cfg.getint('map', 'height') #y
        self.width = cfg.getint('map', 'width') #x
        self.playerNum = cfg.getint('map', 'playerNum')

        #Create map tiles
        self.map = [[0 for y in range(self.height)] for x in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                self.map[x][y] = MapTile(x, y)

    def getMapState(self):
        state = [[0 for y in range(self.height)] for x in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                state[x][y] = self.map[x][y].getTileState()
        return state

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

    def changeTileType(self, tyleType=None):
        self.tileType = tyleType


class TileType:
    def __init__(self):
        self.isWalkable = True
        self.isUnit = False
        self.isStructure = False

    def __repr__(self):
        #return json.dumps(self, default=lambda o: o.__dict__)
        return self.__dict__


def main():
    map = Map()
    mapState = map.getMapState()
    print(mapState[0][0].__dict__)

if __name__ == "__main__":
    main()
