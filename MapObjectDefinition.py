#!/usr/bin/python3

import configparser
import time
from pprint import pprint
import settings as glob

cfg = glob.cfg

class MapObject:
    def __init__(self, height=1, width=1, squareSize=15, name="MapObject", posX=0, posY=0):
        self.height = height #y
        self.width = width #x
        self.squareSize = cfg.getint('map', 'squareSize')
        self.serverRefreshRate = cfg.getint('game', 'serverRefreshRate')
        self.actionNum = 0
        self.isMovable = False
        self.isWalkable = False
        self.texture = None
        self.name = name
        self.isInvulnerable = True
        self.posX = posX
        self.posY = posY
        self.floatPosX = float(posX)
        self.floatPosY = float(posY)

    def setTexture(self, texture):
        self.texture = texture

    def setTileColor(self, tileColor):
        self.tileColor = tileColor

    def incActionNum(self):
        self.actionNum += 1
        return self.actionNum - 1

    def __repr__(self):
        return str(self.name)

class DestructableMapObject(MapObject):
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
    def __init__(self, *args, name="Structure", **kwargs):
        super(Structure, self).__init__(*args, **kwargs)
        self.isStructure = True

class Core(Structure):
    id_num = 0
    def __init__(self, *args, **kwargs):
        self.id_num = Core.id_num
        Core.id_num += 1
        super(Core, self).__init__(*args, name="Core", **kwargs)
        height = cfg.getint('structure.core', 'height')
        width = cfg.getint('structure.core', 'width')
        lifePoint = cfg.getint('structure.core', 'lifePoint')
        
        self.name = "Core"
        self.setTileColor('core')


############
''' UNIT '''
############

class Unit(DestructableMapObject):
    def __init__(self, *args, name="Unit", lifePoint=10, speed=1.0, **kwargs):
        super(Unit, self).__init__(*args, **kwargs)
        self.isWalkable = True
        self.isUnit = True
        self.lifePoint = 10
        self.damage = 5
        self.range = 1
        self.speedX = speed * self.squareSize
        self.speedX = speed * 1.0
        self.speedY = speed * 0.0
        self.lastTimeMoved = time.time()

    def ennemyUnitInRange(self):
        return False

    def attackClosestEnnemy(self):
        pass

    def move(self):
        dx = float(self.speedX) / float(self.serverRefreshRate)
        dy = 0.0

        if self.floatPosX + dx > cfg.getint('map', 'width'):
            dx = cfg.getint('map', 'width') - (self.floatPosX + dx)
            self.floatPosX = cfg.getint('map', 'width') - 1
        else:
            self.floatPosX += dx

        if self.floatPosY + dy > cfg.getint('map', 'height'):
            dy = cfg.getint('map', 'height') - (self.floatPosY + dy)
            self.floatPosY = cfg.getint('map', 'height') - 1
        else:
            self.floatPosY += dy

        glob.the_map.moveObject(self, deltaX=int(dx), deltaY=int(dy))
        self.posX = int(self.floatPosX)
        self.posY = int(self.floatPosY)
        print('speed', dx)

    def behave(self):
        if self.ennemyUnitInRange():
            self.attackClosestEnnemy()
        else:
            self.move()

class MeleUnit(Unit):
    id_num = 0
    def __init__(self, *args, name="Unit",  **kwargs):
        self.id_num = MeleUnit.id_num
        MeleUnit.id_num += 1
        super(MeleUnit, self).__init__(*args, **kwargs)
        height = cfg.getint('unit.meleUnit', 'height')
        width = cfg.getint('unit.meleUnit', 'width')
        lifePoint = cfg.getint('unit.meleUnit', 'lifePoint')
        self.damage = cfg.getint('unit.meleUnit', 'damage')
        self.range = cfg.getint('unit.meleUnit', 'range')
        self.speedX = cfg.getfloat('unit.meleUnit', 'speed') * self.squareSize
        self.speedX = cfg.getfloat('unit.meleUnit', 'speed') * 1.0
        self.speedY = cfg.getfloat('unit.meleUnit', 'speed') * 0.0

        self.name = "knight"
        self.setTileColor('unitMele')

class RangedUnit(Unit):
    id_num = 0
    def __init__(self, *args, name="Unit",  **kwargs):
        self.id_num = RangedUnit.id_num
        RangedUnit.id_num += 1
        super(RangedUnit, self).__init__(*args, **kwargs)
        height = cfg.getint('unit.rangedUnit', 'height')
        width = cfg.getint('unit.rangedUnit', 'width')
        lifePoint = cfg.getint('unit.rangedUnit', 'lifePoint')
        self.damage = cfg.getint('unit.rangedUnit', 'damage')
        self.range = cfg.getint('unit.rangedUnit', 'range')
        self.speedX = cfg.getfloat('unit.rangedUnit', 'speed') * self.squareSize
        self.speedX = cfg.getfloat('unit.rangedUnit', 'speed') * 1.0
        self.speedY = cfg.getfloat('unit.rangedUnit', 'speed') * 0.0

        self.name = "canon"
        self.setTileColor('unitRanged')
