
from socket import *
import time, random, thread,info_receive,Queue,receive_player_information
import xml.etree.ElementTree as ET

PortRecv = 50005
PortSend = 50003
HostIP = "localhost"
lista = Queue.Queue()
listaNewEvent = []


class Cliente():
    def __init__(self,playerPosition):
        try:
            socketRecv = socket(AF_INET, SOCK_STREAM)
            socketRecv.connect((HostIP, PortRecv))
            socketSend = socket(AF_INET, SOCK_STREAM)
            socketSend.connect((HostIP, PortSend))
            self.PlayerNum = socketRecv.recv(1024)
            self.playerPos = playerPosition
            lista.maxsize = 1
            lista.put(self.playerPos)
            thread.start_new_thread(self.recvloop, (socketRecv, ))
            thread.start_new_thread(self.sendloop, (socketSend,self.PlayerNum ))

        except Exception as excp:
            mensaje = excp.message

    def refreshPlayerPosition(self,playerPosition):
        lista.put(playerPosition)

    def hasEvent(self):
        if len(listaNewEvent) != 0:
            return listaNewEvent.pop()
        else:
            return False

    def InfoSendToXml(self,playerNum):
        root = ET.Element('root')

        child = ET.Element('playerNum')
        child.text = playerNum
        root.append(child)

        child = ET.Element('event')
        child.text = "update"
        root.append(child)

        child = ET.Element('position')
        child.text = lista.get()
        root.append(child)

        return ET.tostring(root,"UTF-8")

    def RecvXmlStringToObject(self,data):
        try:

            xml = ET.fromstring(data)
            root = xml.getchildren()

            evento = xml.find('event')
            event = evento.text
  
            positionMonster = xml.find('positionMonster')
            pMons = positionMonster.text

            listPlayers = xml.find('listPlayers')
            list = listPlayers.getchildren()
            returnList = []
            for player in list:
                num = player.xml.find('playerNum')
                num = num.text

                pos = player.xml.find('playerPos')
                pos = pos.text
                playerInfo = receive_player_information.ReceivePlayerInformation(num,pos)
                returnList.append(playerInfo)

            return info_receive.InfoReceive(event,pMons,returnList,PlayerNum)

        except Exception as excp:
            mensaje = excp.message

    def recvloop(self,socketRecv):   
        while 1:
            xmlString = socketRecv.recv(1024)
            infoReceived = self.RecvXmlStringToObject(xmlString)  
            listaNewEvent.append(infoReceived)
            
    def sendloop(self,socketSend,playerNum):
        while 1:
            socketSend.send(self.InfoSendToXml(playerNum))
            time.sleep(0.01)


