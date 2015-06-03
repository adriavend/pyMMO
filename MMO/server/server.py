__author__ = 'Adrian'

from time import sleep

import PodSixNet.Channel
import PodSixNet.Server
import dbcontroller
import clientchannel
import game
import playerserver

class MMOServer(PodSixNet.Server.Server):

    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.db_conn = dbcontroller.DbController()
        self.games = []

        for i in range(2):
            self.games.append(game.Game(i+1))

    channelClass = clientchannel.ClientChannel

    """ Codigo que se ejecuta cuando se conecta un nuevo player. """
    def Connected(self, channel, addr):

        print 'new connection:', channel

        # Enviamos al cliente un mensaje de juego iniciado para que nos envie sus datos de login.
        # En el cliente es el metodo Network_startgame()
        channel.Send({"action": "startgame"})
        print "Pedido de Login..."

    """ Actualiza posicion del player pasado como parametro. """
    def updatemoving(self, map, id, pos_x, pos_y, o, i):
        self.games[map-1].updatemoving(id, pos_x, pos_y, o, i)

    """ Metodo de procesamiento de login del player. """
    def login(self, channel, nickname, password):

        (id_player, number_map) = self.db_conn.retriev(nickname, password)

        if id_player == 0:
            channel.Send({"action": "login", "id_player": 0})
            print "Envio de id 0"
        else:
            channel.Send({"action": "login", "id_player": id_player, "number_map": number_map})
            print "Envio de id exitosamente..."

            player = playerserver.PlayerServer(id_player)
            player.nickname = nickname
            player.password = password
            player.channel = channel

            number_map -= 1 #Restamos uno para acceder a lista de games.

            print "Player creado exitosamente en server. Cant. Players en Linea: ", len(self.games[number_map].players)

            #Al nuevo player le enviamos los datos de los players que ya estan en el mapa.
            for p in self.games[number_map].players:
                channel.Send({"action": "newplayer", "id_player": p.id, "x": p.pos_x, "y": p.pos_y, "nickname": p.nickname})

            #A los players que estan le enviamos para que creen un nuevo player.
            for p in self.games[number_map].players:
                p.channel.Send({"action": "newplayer", "id_player": player.id, "x": 320, "y": 240, "nickname": player.nickname})

            self.games[number_map].players.append(player)

    """
        Metodo que cierra la conexion de un cliente.
        --------------------------------------------
        El procedimiento es el siguiente: El cliente cierra la conexion mediante la llamada conexion.Close(). En el lado
        del servidor solamente recibimos el canal en el metodo Close() de ClientChannel. Lo cual para ello mediante la
        instancia del canal tendremos que obtener en que juego estaba (mapa), cual es posicion en la lista de players y
        que id tiene. Todo ello lo obtenemos mediante self.get_game_pos_idplayer(channel).
        Luego eliminamos el canal de acuerdo a que juego y posicion este.
        Y Finalmente informamos a todos los demas players que eliminen el player pasado como id.
    """
    def Close_channel(self, channel):
        (game, pos, id_player) = self.get_game_pos_idplayer(channel)
        self.del_channel(game, pos)
        print "Player eliminado exitosamente"

        self.Send_delplayer(game, id_player)

    """ Devuelve en que juego, posicion y que id_player es de acuerdo al canal pasado como parametro."""
    def get_game_pos_idplayer(self, channel):
        game = 0

        for g in self.games:
            pos = 0
            for p in g.players:
                if not p.channel == channel:
                    pos += 1
                else:
                    return (game, pos, p.id)
            game += 1

    """ Elimina un player de acuerdo en que juego este y su posicion en la lista de players. """
    def del_channel(self, game, pos):
        del self.games[game].players[pos]

    """ Notificamos a todos los players de un game que eliminen el player con id_player pasado como parametro. """
    def Send_delplayer(self, game, id_player):
        for p in self.games[game].players:
            p.channel.Send({"action": "delplayer", "id_player": id_player})

    # """ Obtiene el canal de acuerdo a la cadena pasada como parametro. """
    # def get_channel(self, channel):
    #     ch = None
    #
    #     for item in self.temp_channels:
    #         if channel == str(item):
    #             ch = item
    #             break
    #
    #     pos = self.get_pos_channel(ch)
    #
    #     self.del_channel(pos)
    #
    #     return ch


    """ Elimina el player del servidor. """
    def Del_player(self, id_player, current_map):
        print "entro a Del_player"
        current_map -= 1
        self.games[current_map].delplayer(id_player)
        self.games[current_map].send_delplayer(id_player)

    def Send_map(self, channel, number_map):
        channel.Send({"action": "map", "map": self.games[number_map-1].map, "background": self.games[number_map-1].background})
        print "Envio de Mapa ..."

    def Send_nextmap(self, number_map, id_player):

        current_map = number_map - 2

        player = self.get_player(current_map, id_player)

        print "Player Obtenido"

        self.del_player(current_map, player)

        print "player eliminado"

        self.Send_delplayer(current_map, player.id)

        next_map = number_map - 1

        self.Send_map(player.channel, number_map)

        #Al nuevo player le enviamos los datos de los players que ya estan en el mapa.
        for p in self.games[next_map].players:
            player.channel.Send({"action": "newplayer", "id_player": p.id, "x": p.pos_x, "y": p.pos_y, "nickname": p.nickname})

        #A los players que estan le enviamos para que creen un nuevo player.
        for p in self.games[next_map].players:
            p.channel.Send({"action": "newplayer", "id_player": player.id, "x": 10, "y": 10, "nickname": player.nickname})

        self.games[next_map].players.append(player)

        print "envio de nuevo mapa"

    def get_player(self, current_map, id_player):
        find = None

        for p in self.games[current_map].players:
            if p.id == id_player:
                find = p
                break

        return find

    def get_posicion_player(self, current_map, player):
        return self.games[current_map].players.index(player)

    def del_player(self, current_map, player):
        del self.games[current_map].players[self.games[current_map].players.index(player)]


print "STARTING SERVER ON LOCALHOST"
mmo_server = MMOServer()
while True:
    mmo_server.Pump()
    sleep(0.01)