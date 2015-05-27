__author__ = 'Adrian'

import PodSixNet.Channel
import PodSixNet.Server
from time import sleep

"""
    Clase que representa un cliente conectado. Representa un canal.. osea un medio para poder enviar y recibir informacion.
"""
class ClientChannel(PodSixNet.Channel.Channel):

    def Network(self, data):
        print data

    """
        Metodo que representa la informacion que envia el cliente al server con la invocacion self.send(data).
        Colocar aca y procesar la informacion quie envia el cliente.
    """
    def Network_place(self, data):
        #self._server = MMOServer !!!!
        self._server.placeMov(int(data["id_player"]), int(data["x"]), int(data["y"]))

class MMOServer(PodSixNet.Server.Server):

    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.players = []
        self.game = None
        self.current_index_player = 0

    channelClass = ClientChannel

    # Codigo que se ejecuta cuando se conecta un nuevo player.
    def Connected(self, channel, addr):
        self.current_index_player += 1 #Si se ejectuta este metodo entonces un cliente se habra conectado.

        print 'new connection:', channel, ' - player: ', self.current_index_player

        #Si el juego no existe ... lo creamos.
        if self.game == None:
            self.game = Game()

        #Enviamos al cliente que se ha conectado el id que le asigno el servidor. En el cliente es el metodo Network_startgame()
        channel.Send({"action": "startgame", "id_player": self.current_index_player, "players": len(self.game.players)})

        player = Player(self.current_index_player, channel)

        #Avisamos a los demas player que un nuevo player se ha conectado.
        for p in self.game.players:
            p.channel.Send({"action": "newplayer", "id_player": self.current_index_player})

        self.game.players.append(player)

    def placeMov(self, id, pos_x, pos_y):
        self.game.placeMov(id, pos_x, pos_y)

"""
    Clase del juego, representar todos los elementos del juego: un par de clientes hasta el momento.
"""
class Game:
    def __init__(self):
        self.players = []

    """
        Cuando el cliente se mueve y envia su posicion este metodo actualiza su poscion d acuerdo al player que sea.
        Tambien se encargara de enviarle a todos los player la posicion de todos los jugadores que hallan en el mapa.
    """
    def placeMov(self, id, pos_x, pos_y):

        find_player = None

        for p in self.players:
            if (p.id == id):
                find_player = p
                break

        find_player.pos_x = pos_x
        find_player.pos_y = pos_y

        for p2 in self.players:
            if (p2 != find_player):
                find_player.channel.Send({"action": "place", "id_player": p2.id, "x": p2.pos_x, "y": p2.pos_y})


"""
    Clase que representa un cliente el cual tiene los datos necesarios para el manejo en el servidor.
"""
class Player:
    def __init__(self, id, channel):
        self.id = id
        self.channel = channel
        self.pos_x = 0
        self.pos_y = 0

print "STARTING SERVER ON LOCALHOST"
mmo_server = MMOServer()
while True:
    mmo_server.Pump()
    sleep(0.01)