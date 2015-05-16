

class Player():
    def __init__(self, pNum,mapNum):
        self.playerNum = pNum
        self.mapaNum = mapNum
        self.x = 0
        self.y = 0

    def getNumber(self):
        return self.playerNum

    def getMapNumber(self):
        return self.mapaNum

    def getPosition(self):
        return position

    def updatePosition(self,x,y):
        self.x = x
        self.y = y