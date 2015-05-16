import monster
import xml.etree.ElementTree as ET,info_receive

listPlayers = []
listMonster = []
number = 0

class Mapa():
    def __init__(self,num):
        self.number = num
        self.mons = monster.Monster()
        listMonster.append(self.mons)

    def step(self):
        for mons in listMonster:
            mons.step()
        info = self.SendInfoToXml()
        return info

    def newPlayerLogIn(player):
        listPlayers.append(player)

    def getNumber(self):
        return self.number

    def update(self,info):
        player1 = filter(lambda x: x.getNumber() == info.getPlayerNum(), playerList)   # se puede implementar una mejora. La clase server tmb tiene la lista de los players conectados
        player1.update(info.getPlayerPos())


    def SendInfoToXml(self):
        root = ET.Element('root')

        event = ET.Element('event')
        event.text = "update"              #ESTA HARDCOREEEEEEE HACER UNA ENUM
        root.append(event)

        positionMonster = ET.Element('positionMonster')
        positionMonster.text = self.mons.getPosition()
        root.append(positionMonster)

        nodeListPlayers = ET.Element('listPlayers')   #nodo que va a tener a todos los players

        for player in listPlayers:
            nodePlayer = ET.Element('Player')    #un nodo por cada player con su info
            nodeListPlayers.append(nodePlayer)

            playerNum = ET.Element('playerNum')
            playerNum.text = str(player.getNumber())
            nodePlayer.append(playerNum)

            playerPos = ET.Element('playerPos')
            playerPos.text = player.getPosition()
            nodePlayer.append(playerPos)

        root.append(nodeListPlayers)

        return ET.tostring(root,"UTF-8")