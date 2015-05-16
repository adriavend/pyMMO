

class InfoReceive():
    """description of class"""
    def __init__(self,playerNum,evento,monsterPosition,listPlayers,thisPlayerNum):
        self.event = evento
        self.monsterPosition = monsterPosition
        self.listPlayers = listPlayers
        pass

    def getEvent(self):
        return self.event

    def getMonsterPosition(self):
         posmonsterX = str(self.monsterPosition[:2:])
         posmonsterY = str(self.monsterPosition[3::])
         return posmonsterX,posmonsterY

    def getOtherPlayerPos(self):
         for player in self.listPlayers:
             if(player.getPlayerNum() != thisPlayerNum):
                 return player.getPlayerPosition()

