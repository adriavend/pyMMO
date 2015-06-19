__author__ = 'Adrian'

import config
import funciones
import random
import monsterserver
import threading
import time
import pygame

"""
    Clase del juego, representar todos los elementos del juego: un par de clientes hasta el momento.
"""
class Game(threading.Thread):
    """
    Constructor de la clase.
    """
    def __init__(self, id_mapa):
        threading.Thread.__init__(self)
        path = "%smap_%s.txt" % (config.PATH_MAPS, str(id_mapa))
        self.map = funciones.leer_mapa(path)
        print "Mapa %s creado exitosamente ..." % (id_mapa)

        self.background = "back_game_%s.gif" % (id_mapa)
        self.players = []
        self.monsters = []
        self.init_monsters()
        self.clock = pygame.time.Clock()

    """ Crea e inicializa a los moustros del mapa (game). """
    def init_monsters(self):
        row = len(self.map)
        col = len(self.map[0])

        amount = 0 ##random.randrange(2, 10) #Cantidad de moustro a generar.
        count = 0

        while count != amount:
            rf = random.randrange(row)
            rc = random.randrange(col)

            if self.map[rf][rc] == '.':
                self.map[rf][rc] = 'M'
                count +=1
                orientation = random.randrange(1, 5) #Genera valores de 1 ... 4.
                pending_mov = random.randrange(config.MIN_MOVE, config.MAX_MOVE)
                self.monsters.append(monsterserver.MonsterServer(count, rf, rc, orientation, pending_mov))
                # print "moustro generado o:", orientation, "mov:", pending_mov

        print len(self.monsters), "Moustros Aleatorios Generados Exitosamente ..."

    """ Metodo run(). Contiene la logica de movimientos de los moustros. Esto es un hilo aparte."""
    def run(self):
        rows = len(self.map) - 1
        columns = len(self.map[0]) - 1

        for m in self.monsters:
            m.is_moving = False

            while not m.is_moving:
                band = False

                if m.do_move == 0:
                    self.monster_restart_move(m)

                if m.orientation == 1:
                    if m.j+1 < columns:
                        if self.map[m.i][m.j+1] == '.':
                            band = True
                elif m.orientation == 2:
                    if m.j-1 > 0:
                        if self.map[m.i][m.j-1] == '.':
                            band = True
                elif m.orientation == 3:
                    if m.i+1 < rows:
                        if self.map[m.i+1][m.j] == '.':
                            band = True
                elif m.orientation == 4:
                    if m.i-1 > 0:
                        if self.map[m.i-1][m.j] == '.':
                            band = True

                if band:
                    self.update_monster_map(m)
                else:
                    self.monster_restart_move(m)
        self.time = self.clock.tick(20)
        # time.sleep(0.2)

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

        for m in self.monsters:
            find_player.channel.Send({"action": "updatemonters", "id_monster": m.id, "x": m.j * config.TAB_GAME, "y": m.i * config.TAB_GAME, "orientation": m.orientation, "t": m.t})

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

    """ Reinicia el movimiento del moustro. """
    def monster_restart_move(self, m):
        m.orientation = random.randrange(1, 5)
        m.do_move = random.randrange(config.MIN_MOVE, config.MAX_MOVE)

    """ Cambia el movimiento del moustro y actualiza el mapa. """
    def update_monster_map(self, m):

        self.map[m.i][m.j] = '.'
        m.do_move -= 1
        m.is_moving = True

        i = m.i
        j = m.j

        m.t += 1
        if m.t > 1:
            m.t = 0

        if m.orientation == 1:
            self.map[i][j+1] = 'M'
            m.j += 1
        elif m.orientation == 2:
            self.map[i][j-1] = 'M'
            m.j -= 1
        elif m.orientation == 3:
            self.map[i+1][j] = 'M'
            m.i += 1
        elif m.orientation == 4:
            self.map[i-1][j] = 'M'
            m.i -= 1

        print "Moustro", m.id, "se ha movido exitosamente. Orientacion", m.orientation, "Coordenadas: ", (m.i, m.j)
