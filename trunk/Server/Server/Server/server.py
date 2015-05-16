#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import *
import time, thread, random, monster,mapa,client_number,datetime,xml,Queue,player
Clients = {}
Clientsonline = []

Port = 50005
Port2  = 50003
HostIP = ""
dummy = ""

Outtube, Intube, Worktube = [], [], []

ListMaps = []
SendList = []
RecvQueue = Queue.Queue()
listPlayers = []

def main():
    #readdatabase()
    thread.start_new_thread(acceptconthread, (dummy, ))
    generarMundo()
    thread.start_new_thread(step, (dummy, ))
    while 1:
        workthrough()

def processReceivedInfo(info,playerNum):
    if info.getEvent() == "update":
        player1 = filter(lambda x: x.getNumber() == playerNum, listPlayers)
        map = ListMaps[player1.getMapNumber()]
        map.update(info)  #actualiza la posicion del player en ese mapa

# Ciclo principal
def workthrough():
    try: 
        while 1:
            for map in ListMaps:   #actualizar la info que se manda de cada mapa
               pass

    except Exception as excp:
        mensaje = excp.message  

        
        #if len(Worktube) > 0:
        #    if Worktube[0][1] == "upd":
        #        newlist = Clientsonline[:]
        #        newlist2 = " ".join(newlist)
        #        Outtube.append([Worktube[0][0], "upd", newlist2])
        #        Worktube.pop(0)  #  .POP: Quita el ítem en la posición dada de la lista, y lo devuelve. Si no se especifica un índice, lista.pop() quita y devuelve el último ítem de la lista.
        #if len(Worktube) > 0:
        #    if Worktube[0][1] == "say":
        #        Worktube[0][2] = "%s %s" % (Worktube[0][0], Worktube[0][2])
        #        for client in Clientsonline:
        #            Outtube.append([client, "say", Worktube[0][2]])
        #        Worktube.pop(0)
        #if len(Intube) > 0:
        #    if Intube[0][1] == "say":
        #        naostring = " ".join(Intube[0][2])    #"str".join(lista)   A cada elemento de la lista lo convierte en un string y lo separa con ese "str"
        #        Worktube.append([Intube[0][0], "say", naostring])
        #        Intube.pop(0)

def generarMundo():
    for i in range(3):
        map = mapa.Mapa(i)
        ListMaps.append(map)
    step(dummy)


def step(dummy):
    try:
        for map in ListMaps:
            SendList.clear()
            SendList.insert(map.getNumber(),map.step())

        time.sleep(0.01)
    except Exception as excp:
        mensaje = excp.message


def acceptconthread(dummy):
    soc = socket(AF_INET, SOCK_STREAM)
    soc.bind((HostIP, Port))
    soc.listen(100)
    while 1:
        conn, addr = soc.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        thread.start_new_thread(connectingThread, (conn, addr))
 
def connectingThread(conn, addr):
    try:
        clientNumber = client_number.ClientNumber()
        num = clientNumber.getNumber()    

        soc2 = socket(AF_INET, SOCK_STREAM)
        soc2.bind((HostIP, Port2))
        soc2.listen(100)
        conn2, addr2 = soc2.accept()
        newPlayer = player.Player(num,0)
        listPlayers.append(newPlayer)
        thread.start_new_thread(sendloop, (num, conn, addr))
        thread.start_new_thread(recvloop, (num, conn2, addr2))

    except Exception as excp:
        mensaje = excp.message
        #log = open("c:/Facultad/Arquitectura de Software/log"+str(datetime.now().microsecond)+".txt","w")
        #log.write("MENSAJE: \n")
        #log.write(excp.message)
        #log.close()
 

def sendloop(playerNum, conn, addr):
    try:
        conn.send(str(playerNum))
        while 1:
            sendInfo = SendList[0]  #va el numero de mapa
            conn.send(sendInfo)
    except Exception as excp:
        mensaje = excp.message
        #bbb = Clientsonline.remove(name)

   
 
def recvloop(playerNum, conn2, addr2):
    try:
        while 1:
            data = conn2.recv(1024)
            receivedInfo = RecvXmlToObject(data)
            processReceivedInfo(ReceivedInfo,playerNum)      
    except:
        print playerNum, "has disconnected"
 

def RecvXmlToObject(data):
    xml = ET.fromstring(data)
    root = xml.getchildren()

    playerNum = xml.find('playerNum')
    pNum = playerNum.text

    event = xml.find('event')
    evento = event.text
  
    position = xml.find('position')
    pos = position.text

    return info_receive.InfoReceive(pNum,evento,pos)
 
###################################### DATABASE ################################

#def writedatabase():
#    try:
#        f = open("database", "r+")
#    except:
#        f = open("database", "w")
#        f.close()
#        print "database created"
#        f = open("database", "r+")
#    for element in Clients:
#        savestring = ""
#        for item in Clients[element][0]:
#            savestring = "%s%s " % (savestring, item)
#        savestring = "%s\n" % savestring
#        f.write(savestring)
#    f.close()
#    print "database saved"
 
#def readdatabase():
#    try:
#        f = open("database", "r+")
#        for line in f:
#            g = line.split()
#            name = g[0]
#            Clients[name] = [[name], ["conn", "addr"], ["conn2", "addr2"]]
#            g.pop(0)
#            for element in g:
#                Clients[name][0].append(element)
#    except:
#        print "couldnt read database"
 
#def saveloop(dummy):
#    while 1:
#        time.sleep(120)
#        writedatabase()
 

if __name__ == "__main__":
    main()


