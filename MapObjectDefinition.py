#!/usr/bin/python3

import configparser
from pprint import pprint

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

class MapObject:
    def __init__(self, height=1, width=1, name="MapObject"):
        self.height = height #y
        self.width = width #x
        self.isMovable = False
        self.texture = None
        self.name = name
        self.isInvulnerable = True

    def setTexture(self, texture):
        self.texture = texture

    def __repr__(self):
        return str(self.name)

class DestructableMapObject(MapObject):
    def __init__(self, height=1, width=1, name="DestructableMapObject", lifePoint=100):
        MapObject.__init__(self, height, width, name)
        self.lifePoint = lifePoint
        self.isInvulnerable = False

    def getLifePoint(self):
        return self.lifePoint
    def setLifePoint(self, lifePoint):
        self.lifePoint = lifePoint

#################
''' STRUCTURE '''
#################

class Structure(DestructableMapObject):
    def __init__(self, height=1, width=1, name="Structure", lifePoint=100):
        DestructableMapObject.__init__(self, height, width, name, lifePoint)

class Core(Structure):
    def __init__(self, name="Core"):
        height = cfg.getint('structure.core', 'height')
        width = cfg.getint('structure.core', 'width')
        lifePoint = cfg.getint('structure.core', 'lifePoint')
        Structure.__init__(self, height, width, name, lifePoint)
        
        self.setTexture('green')


############
''' UNIT '''
############

class Unit(DestructableMapObject):
    def __init__(self, height=1, width=1, name="Unit", lifePoint=10):
        DestructableMapObject.__init__(self, height, width, name, lifePoint)

class meleUnit(Unit):
    def __init__(self, name="meleUnit"):
        height = cfg.getint('unit.meleUnit', 'height')
        width = cfg.getint('unit.meleUnit', 'width')
        lifePoint = cfg.getint('unit.meleUnit', 'lifePoint')
        self.dammage = cfg.getint('unit.meleUnit', 'dammage')
        self.range = cfg.getint('unit.meleUnit', 'range')

        Unit.__init__(self, height, width, name, lifePoint)

class rangedUnit(Unit):
    def __init__(self, name="rangedUnit"):
        height = cfg.getint('unit.rangedUnit', 'height')
        width = cfg.getint('unit.rangedUnit', 'width')
        lifePoint = cfg.getint('unit.rangedUnit', 'lifePoint')
        self.dammage = cfg.getint('unit.rangedUnit', 'dammage')
        self.range = cfg.getint('unit.rangedUnit', 'range')

        Unit.__init__(self, height, width, name, lifePoint)
