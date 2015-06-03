__author__ = 'Adrian'

import config
import funciones
import random

"""
    Clase del juego, representar todos los elementos del juego: un par de clientes hasta el momento.
"""
class Game:
    def __init__(self, id_mapa):
        path = "%smap_%s.txt" % (config.PATH_MAPS, str(id_mapa))
        self.map = funciones.leer_mapa(path)
        print "Mapa %s creado exitosamente ..." % (id_mapa)

        self.generate_monsters()

        self.background = "back_game_%s.gif" % (id_mapa)
        self.players = []

    def generate_monsters(self):
        fil = len(self.map)
        col = len(self.map[0])

        cant = random.randrange(2, 20)
        count = 0

        while count != cant:
            rf = random.randrange(fil)
            rc = random.randrange(col)

            if self.map[rf][rc] == '.':
                self.map[rf][rc] = 'M'
                count +=1

        print cant, "Moustros Aleatorios Generados Exitosamente ..."


    """
        Cuando el cliente se mueve y envia su posicion este metodo actualiza su poscion d acuerdo al player que sea.
        Tambien se encargara de enviarle a todos los player la posicion de todos los jugadores que hallan en el mapa.
    """
    def updatemoving(self, id, pos_x, pos_y, o, i):

        find_player = None

        for p in self.players:
            if (p.id == id):
                find_player = p
                break

        find_player.pos_x = pos_x
        find_player.pos_y = pos_y
        find_player.orientation = o
        find_player.image = i

        for p2 in self.players:
            if (p2 != find_player):
                find_player.channel.Send({"action": "updateplayers", "id_player": p2.id, "x": p2.pos_x, "y": p2.pos_y, "orientation": p2.orientation, "t": p2.image})

    """ Busca y elimina una player del juego. """

    def delplayer(self, id_player):
        pos = 0

        for p in self.players:
            print "entro "
            if not p.id == id_player:
                pos +=1
            else:
                break

        del self.players[pos]

        print "se elimino"

    """ Notifica a todos los players del juego que jugador (id) se ha desconectado. """
    def send_delplayer(self, id):
        for p in self.players:
            p.channel.Send(({"action": "delplayer", "id_player": id}))
            print "envio de del player"


