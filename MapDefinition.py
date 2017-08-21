#!/usr/bin/env/python3

import configparser
import json
from pprint import pprint

import settings as glob
import MapObjectDefinition
from utils import ActionEvent, ActionEventManager, MyEncoder

cfg = glob.cfg


class Map:
    def __init__(self):
        self.height = cfg.getint('map', 'height') #y
        self.width = cfg.getint('map', 'width') #x
        self.squareSize = cfg.getint('map', 'squareSize')
        self.playerNumber = cfg.getint('map', 'playerNumber')
        self.playerWidthZone = cfg.getint('map', 'playerWidthZone')

        #Create map tiles
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
        glob.actionEventManager.add_construction_event(objectToBePlaced, (x, y))

    def moveObject(self, objectToMove, deltaX=1, deltaY=0):
        startX = objectToMove.posX
        startY = objectToMove.posY
        emptyObject = MapTile(startX, startY, isPlayerZone=self.isCoordInPlayerZone(startX, startY))
        modif_emptyObj = self.map[startX][startY].changeTileType(emptyObject.tileType)
        modif_emptyObj_json = MyEncoder().encode(modif_emptyObj)

        endX = startX + deltaX
        endY = startY + deltaY

        if endX >= self.width-1 or endY >= self.height-1:
            print('moveOutOfBound')
            glob.actionEventManager.add_kill_event(objectToMove)
        self.map[endX][endY].changeTileType(objectToMove)
        glob.actionEventManager.add_move_event(objectToMove, (endX, endY))

        
    def __repr__(self):
        return MyEncoder().encode(self.map)


class MapTile:
    def __init__(self, x, y, playerNumber=2, isPlayerZone=False):
        self.x = x
        self.y = y
        self.isPlayerZone = isPlayerZone
        self.tileType = TileType(isPlayerZone)
        self.isRevealedForPlayer = [ False for x in range(playerNumber) ]

    def __repr__(self):
        return MyEncoder().encode(self.tileType)

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

