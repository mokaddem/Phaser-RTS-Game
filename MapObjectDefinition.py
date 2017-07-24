#!/usr/bin/python3

import configparser
from pprint import pprint

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

class MapObject:
    def __init__(self, height=1, width=1, name="MapObject", posX=0, posY=0):
        self.height = height #y
        self.width = width #x
        self.isMovable = False
        self.isWalkable = False
        self.texture = None
        self.name = name
        self.isInvulnerable = True

    def setTexture(self, texture):
        self.texture = texture

    def setTileColor(self, tileColor):
        self.tileColor = tileColor

    def __repr__(self):
        return str(self.name)

class DestructableMapObject(MapObject):
    #def __init__(self, height=1, width=1, name="DestructableMapObject", lifePoint=100, player=1):
        #MapObject.__init__(self, height, width, name)
    def __init__(self, *args, lifePoint=100, player=1, **kwargs):
        super(DestructableMapObject, self).__init__(*args, **kwargs)
        self.lifePoint = lifePoint
        self.isInvulnerable = False
        self.isUnit = False
        self.isStructure = False
        self.player = player

    def getLifePoint(self):
        return self.lifePoint
    def setLifePoint(self, lifePoint):
        self.lifePoint = lifePoint
    def applyDamage(self, dmg):
        self.lifePoint = self.lifePoint - dmg

#################
''' STRUCTURE '''
#################

class Structure(DestructableMapObject):
    #def __init__(self, height=1, width=1, name="Structure", lifePoint=100, player=1):
    #    DestructableMapObject.__init__(self, height, width, name, lifePoint, player)
    def __init__(self, *args, name="Structure", **kwargs):
        super(Structure, self).__init__(*args, **kwargs)
        self.isStructure = True

class Core(Structure):
    #def __init__(self, name="Core", player=1):
    def __init__(self, *args, **kwargs):
        height = cfg.getint('structure.core', 'height')
        width = cfg.getint('structure.core', 'width')
        lifePoint = cfg.getint('structure.core', 'lifePoint')
        #Structure.__init__(self, height, width, name, lifePoint, player)
        super(Core, self).__init__(*args, name="Core", **kwargs)
        
        self.setTileColor('core')


############
''' UNIT '''
############

class Unit(DestructableMapObject):
    #def __init__(self, height=1, width=1, name="Unit", lifePoint=10, player=1):
    #    DestructableMapObject.__init__(self, height, width, name, lifePoint)
    def __init__(self, *args, name="Unit", lifePoint=10,  **kwargs):
        super(Unit, self).__init__(*args, **kwargs)
        self.isWalkable = True
        self.isUnit = True
        self.lifePoint = 10
        self.damage = 5
        self.range = 1

    def behave(self):
        if self.ennemyUnitInRange():
            self.attackClosestEnnemy()
        else:
            self.move()

class MeleUnit(Unit):
    #def __init__(self, name="meleUnit", player=1):
    def __init__(self, *args, name="Unit",  **kwargs):
        height = cfg.getint('unit.meleUnit', 'height')
        width = cfg.getint('unit.meleUnit', 'width')
        lifePoint = cfg.getint('unit.meleUnit', 'lifePoint')
        self.damage = cfg.getint('unit.meleUnit', 'damage')
        self.range = cfg.getint('unit.meleUnit', 'range')

        #Unit.__init__(self, height, width, name, lifePoint)
        super(MeleUnit, self).__init__(*args, **kwargs)

        self.setTileColor('unitMele')

class RangedUnit(Unit):
    #def __init__(self, name="rangedUnit", player=1):
    def __init__(self, *args, name="Unit",  **kwargs):
        height = cfg.getint('unit.rangedUnit', 'height')
        width = cfg.getint('unit.rangedUnit', 'width')
        lifePoint = cfg.getint('unit.rangedUnit', 'lifePoint')
        self.damage = cfg.getint('unit.rangedUnit', 'damage')
        self.range = cfg.getint('unit.rangedUnit', 'range')

        #Unit.__init__(self, height, width, name, lifePoint)
        super(RangedUnit, self).__init__(*args, **kwargs)

        self.setTileColor('unitRanged')
