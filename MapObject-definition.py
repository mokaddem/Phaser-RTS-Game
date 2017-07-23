#!/usr/bin/python3

import configparser
from pprint import pprint

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
    def __init__(self, height=1, width=1, name="Structure", lifePoint=100)):
        DestructableMapObject.__init__(self, height, width, name, lifePoint)

class Core(Structure):
    def __init__(self, name="Core"):
        self.height = cfg.getint('structure.core', 'height')
        self.width = cfg.getint('structure.core', 'width')
        self.lifePoint = cfg.getint('structure.core', 'lifePoint')
        Structure.__init__(self, height, width, name, lifePoint)


############
''' UNIT '''
############

class Unit(DestructableMapObject):
    def __init__(self, height=1, width=1, name="Unit", lifePoint=10)):
        DestructableMapObject.__init__(self, height, width, name, lifePoint)

class meleUnit(Unit):
    def __init__(self, name="meleUnit"):
        self.height = cfg.getint('unit.meleUnit', 'height')
        self.width = cfg.getint('unit.meleUnit', 'width')
        self.lifePoint = cfg.getint('unit.meleUnit', 'lifePoint')
        self.dammage = cfg.getint('unit.meleUnit', 'dammage')
        self.range = cfg.getint('unit.meleUnit', 'range')

        Unit.__init__(self, height, width, name, lifePoint)

class rangedUnit(Unit):
    def __init__(self, name="rangedUnit"):
        self.height = cfg.getint('unit.rangedUnit', 'height')
        self.width = cfg.getint('unit.rangedUnit', 'width')
        self.lifePoint = cfg.getint('unit.rangedUnit', 'lifePoint')
        self.dammage = cfg.getint('unit.rangedUnit', 'dammage')
        self.range = cfg.getint('unit.rangedUnit', 'range')

        Unit.__init__(self, height, width, name, lifePoint)
