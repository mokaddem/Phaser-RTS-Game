from json import JSONEncoder

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

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


class Player:
    def __init__(self, num):
        self.num = num
        self.ready = False

    def setReady(self):
        self.ready = True

    def isReady(self):
        return self.ready
