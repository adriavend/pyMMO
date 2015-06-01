__author__ = 'Adrian'

from time import sleep

import PodSixNet.Channel
import PodSixNet.Server
import db_controller
import funciones
import config

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
    def Network_updatemoving(self, data):
        #self._server = MMOServer !!!!
        self._server.updatemoving(int(data["id_player"]), int(data["x"]), int(data["y"]), int(data["orientation"]), int(data["t"]))

    """ Metodo que recibe los datos de login del player para iniciarse y los envia al servidor. """
    def Network_login(self, data):
        nickname = data["nickname"]
        password = data["password"]
        channel = data["channel"]

        self._server.login(channel, nickname, password)

    """ Metodo que se ejecuta cuando en el cliente llama a 'connection.Close()'. """
    def Close(self):
        self._server.Del_player(self)

    """ Metodo que el cliente pide el mapa. """
    def Network_map(self, data):
        self._server.Send_map(self)

"""
    SERVER !!!
"""
class MMOServer(PodSixNet.Server.Server):

    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.db_conn = db_controller.DbController()
        self.temp_channels = []
        self.game = Game()

    channelClass = ClientChannel

    """ Codigo que se ejecuta cuando se conecta un nuevo player. """
    def Connected(self, channel, addr):

        print 'new connection:', channel

        # Enviamos al cliente que se ha conectado el channel (en string).
        # En el cliente es el metodo Network_channel()
        channel.Send({"action": "channel", "channel": str(channel)})
        print "Envio de canal...:"

        # list_test = ["a", "b", "mpilgrim", "z", "example"]
        # channel.Send({"action": "test", "list": list_test})
        # print "Envio de lista test ..."

        self.temp_channels.append(channel)

    """ Actualiza posicion del player pasado como parametro. """
    def updatemoving(self, id, pos_x, pos_y, o, t):
        self.game.updatemoving(id, pos_x, pos_y, o, t)

    """ Metodo de procesamiento de login del player. """
    def login(self, channel, nickname, password):

        ch = self.get_channel(channel)

        id_player = self.db_conn.retriev(nickname, password)

        if id_player == 0:
            ch.Send({"action": "login", "id_player": 0})
            print "Envio de id 0"
        else:
            ch.Send({"action": "login", "id_player": id_player})
            print "Envio de id exitosamente..."

            player = PlayerServer(id_player)
            player.nickname = nickname
            player.password = password
            player.channel = ch

            print "Player creado exitosamente en server. Cant. Players en Linea: ", len(self.game.players)

            #Colocar aca el envio de los demas players al player nuevo.
            for p in self.game.players:
                ch.Send({"action": "newplayer", "id_player": p.id, "x": p.pos_x, "y": p.pos_y, "nickname": p.nickname})

            #Informamos a los demas players que un player nuevo se ha conectado
            for p in self.game.players:
                p.channel.Send({"action": "newplayer", "id_player": player.id, "x": 320, "y": 240, "nickname": player.nickname})

            self.game.players.append(player)

    """ Obtiene el canal de acuerdo a la cadena pasada como parametro. """
    def get_channel(self, channel):
        ch = None

        for item in self.temp_channels:
            if channel == str(item):
                ch = item
                break

        pos = self.get_pos_channel(ch)

        self.del_channel(pos)

        return ch

    """ Elimina un canal de la lista. """
    def del_channel(self, pos):
        del self.temp_channels[pos]

    """ Devuelve la posicion del canal en la lista, pasada como parametro. """
    def get_pos_channel(self, channel):
        return self.temp_channels.index(channel)

    """ Elimina el player del servidor. """
    def Del_player(self, channel):
        self.game.delplayer(channel)

    def Send_map(self, channel):
        channel.Send({"action": "map", "map": self.game.map, "background": self.game.background})
        print "Envio de Mapa ..."
"""
    Clase del juego, representar todos los elementos del juego: un par de clientes hasta el momento.
"""
class Game:
    def __init__(self):
        self.map = funciones.leer_mapa(config.PATH_MAPS+"map_1.txt")
        print "Mapa leido exitosamente ..."
        self.background = "back_game_1.gif"

        self.players = []

    """
        Cuando el cliente se mueve y envia su posicion este metodo actualiza su poscion d acuerdo al player que sea.
        Tambien se encargara de enviarle a todos los player la posicion de todos los jugadores que hallan en el mapa.
    """
    def updatemoving(self, id, pos_x, pos_y, o, t):

        find_player = None

        for p in self.players:
            if (p.id == id):
                find_player = p
                break

        find_player.pos_x = pos_x
        find_player.pos_y = pos_y
        find_player.orientation = o
        find_player.t = t

        for p2 in self.players:
            if (p2 != find_player):
                find_player.channel.Send({"action": "updateplayers", "id_player": p2.id, "x": p2.pos_x, "y": p2.pos_y, "orientation": p2.orientation, "t": p2.t})

    """ Busca y elimina una player del juego. """
    def delplayer(self, channel):
        pos = 0
        p_id = 0

        for p in self.players:
            if not p.channel == channel:
                pos +=1
            else:
                p_id = p.id
                break

        del self.players[pos]

        self.send_delplayer(p_id)

    """ Notifica a todos los players del juego que jugador (id) se ha desconectado. """
    def send_delplayer(self, id):
        for p in self.players:
            p.channel.Send(({"action": "delplayer", "id_player": id}))

"""
    Clase que representa un cliente el cual tiene los datos necesarios para el manejo en el servidor.
"""
class PlayerServer:
    def __init__(self, id):
        self.id = id
        self.channel = None
        self.pos_x = 0
        self.pos_y = 0
        self.map = 1
        self.nickname = ""
        self.password = ""
        self.t = 0
        self.orientation = 0

print "STARTING SERVER ON LOCALHOST"
mmo_server = MMOServer()
while True:
    mmo_server.Pump()
    sleep(0.01)