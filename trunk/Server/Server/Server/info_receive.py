


class InfoReceive(object):
    """description of class"""
    def __init__(self,playerNum,event,position):
        self.playerNum = playerNum
        self.event = event
        self.position = position
        pass

    def getPlayerNum(self):
        return self.playerNum

    def getEvent(self):
        return self.event

    def getPlayerPos(self):
         X = str(self.position[:2:])
         Y = str(self.position[3::])
         return X,Y