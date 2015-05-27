__author__ = 'Adrian'

import PodSixNet.Channel
import PodSixNet.Server
from time import sleep

class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print data

class MMOServer(PodSixNet.Server.Server):

    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.players = []
        self.game = None
        self.current_index_player = 0

    channelClass = ClientChannel

    # Codigo que se ejecuta cuando se conecta un nuevo player.
    def Connected(self, channel, addr):
        self.current_index_player+=1
        print 'new connection:', channel, ' - player: ', self.current_index_player





"""
Clase de juegos, que representara todos los elementos del juego: un par de clientes, el mapa bordo y quien es el turno.
"""
class Game:
    def __init__(self, players):
        self.players = players

print "STARTING SERVER ON LOCALHOST"
mmo_server = MMOServer()
while True:
    mmo_server.Pump()
    sleep(0.01)
