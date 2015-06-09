#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from time import sleep

import pygame
from PodSixNet.Connection import ConnectionListener, connection

from client import fondo, config, mounstro, player, scene
import map


class SceneGame(scene.Scene, ConnectionListener):
    def __init__(self, nickname, password):
        scene.Scene.__init__(self)

        pygame.mouse.set_visible(False)

        # Velocidades del Juego
        self.vx, self.vy = (0, 0)

        self.left_sigueapretada, self.right_sigueapretada, self.up_sigueapretada, self.down_sigueapretada = False, False, False, False

        self.fondo = fondo.Fondo(config.PATH_BACKS + "none.gif")
        self.map_number = 1
        self.map = None #map.Map(config.PATH_MAPS + "map_1.txt")
        self.player_1 = player.Player(0, nickname)
        self.others_players = []
        self.monsters = []
        self.t = 0
        self.font = pygame.font.Font(None, 92)

        # PARTE SERVER
        # 1º) Nos conectamos.
        self.Connect() #Sobre carga host and port.

        self.nickname = nickname
        self.password = password

        self.execute_sequence = 0
        self.run = False

        # FIN PARTE SERVER>

    def on_update(self):

        # PARTE SERVER

        connection.Pump()
        self.Pump()

        # FIN PARTE SERVER>

        if not self.run: return

        """
         Logica del Juego. Manejo de Movimientos y Colisiones.
         """
        # 1°) Movemos el fondo y las paredes sin importar que halla o no colisiones. Ojo el player no se mueve
        self.moving()

        # 2°) Ahora comprobamos si realmente hay colision entre el player con algun muro.
        # En caso de existir colision -> Movemos en sentido contrario (volviendo a la posicion original que tenia antes)
        if self.player_1.is_collision_brick(self.map.list_brick):
            self.fondo.update(-self.vx, -self.vy)
            self.map.update(-self.vx, -self.vy)
            # self.moving_monster(-self.vx, -self.vy)
        elif self.player_1.is_collision_players(self.others_players):
            self.player_1.update(-self.vx, -self.vy, self.t)
            self.fondo.update(-self.vx, -self.vy)
            self.map.update(-self.vx, -self.vy)
            # self.moving_monster(-self.vx, -self.vy)
        elif self.player_1.is_collision_monsters(self.monsters):
            self.fondo.update(-self.vx, -self.vy)
            self.map.update(-self.vx, -self.vy)
            # self.moving_monster(-self.vx, -self.vy)
            self.player_1.change_image_explosion()
            config.QUIT_FLAG = True
            """
                Envia la señal de desconexion al server para que nos borre del mismo.
                Esto se procesara en el metedo Close() de ClientChannel.
            """
            connection.Close()
            print self.print_sequence(), "Desconetado del Server..."
        elif self.player_1.is_collision_port(self.map.port):
            self.player_1.rect.top = 10
            self.player_1.rect.left = 10
            self.others_players = []

            self.map_number += 1
            self.next_map(self.map_number, self.player_1.id)
        else:
            # 3°) Ahora comprobamos que si el fondo se mueve saliendose de la pantalla entonces que se empieze a mover el player
            if self.fondo.rect.left > 0 \
                    or self.fondo.rect.right < config.SCREEN_WIDTH \
                    or self.fondo.rect.top > 0 \
                    or self.fondo.rect.bottom < config.SCREEN_HEIGHT:  # Si el fondo se quiere desprender de la izquierda de la pantalla or de la derecha o arriba o abajo.
                self.fondo.update(-self.vx, -self.vy)  #No se mueve. Regrega una direccion
                self.map.update(-self.vx, -self.vy)  # No se mueve. Regrega una direccion
                # self.moving_monster(-self.vx, -self.vy)
                self.player_1.update(self.vx, self.vy, self.t)  # Se mueve. Porque nunca le indicamos que se moviera
            else:
                self.player_1.update(self.vx / 2, self.vy / 2,
                                     self.t)  # self.vx/2 reduce la velocidad a la mitad para que puede ir al medio de la pantalla.

            # Controlamos que el player no se salga de la pantalla. Caso contrario volvemos una direccion
            if self.player_1.rect.left == 0 \
                    or self.player_1.rect.right > config.SCREEN_WIDTH \
                    or self.player_1.rect.top == 0 \
                    or self.player_1.rect.bottom > config.SCREEN_HEIGHT:
                self.player_1.update(-self.vx, -self.vy, self.t)
        #---------------------------------------------------------------------------------------------------------

        if self.run:
            """
             A continuacion se detalle la logica del posicionamiento.
             Debido a que el fondo es el que se mueve. Entonces debemos plantear un eje de coordenadas de acuerdo al fondo
             y al eje de coordenadas que nos proporciona la ventana. Esto es por lo siguiente:
             - Nos interesa la posicion x e y que tenga el player con respecto al fondo y no a la ventana porque el otro cliente
             tiene que actualizar su posicion de acuerdo a que punto del mapa se encuentra y no al punto de su ventana
             (que sera distinto entre todos los cliente).
             - Todos los player tendran su ventana en cualquier parte del fondo lo cual significa que no se pueda respetar
             el eje x e y de la ventana.
             Se ha planteado una funcion que devuelve la posicion x e y con respecto al fondo. Debemos tener en cuenta
             que la posicion del fondo en cada ventana del player sera nuestra variable en la funcion de posicionamiento x e y.
             Formula:
             * Obtener posicion x e y con respecto al fondo
             x = abs(self.fondo_1.rect.left) + self.player_1.rect.left
             y = abs(self.fondo_1.rect.top) + self.player_1.rect.top
             * Obtenencion de x e y en la otra ventana de todos los clientes de acuerdo en que posicion esten SUS fondos.
             other_player.server_update(self.fondo_1.rect.left + x, self.fondo_1.rect.top + y)
             """
            x = abs(self.fondo.rect.left) + self.player_1.rect.left
            y = abs(self.fondo.rect.top) + self.player_1.rect.top

            self.Send({"action": "updatemoving", "map": self.map_number, "x": x, "y": y, "id_player": self.player_1.id, "orientation": self.player_1.orientation, "image": self.player_1.image_current})
            sleep(0.01)

    def on_event(self, events):
        speed_game = config.SPEED_GAME

        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left_sigueapretada = True
                    self.vx = - speed_game
                if event.key == pygame.K_RIGHT:
                    self.right_sigueapretada = True
                    self.vx = speed_game
                if event.key == pygame.K_UP:
                    self.up_sigueapretada = True
                    self.vy = - speed_game
                if event.key == pygame.K_DOWN:
                    self.down_sigueapretada = True
                    self.vy = speed_game

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.vx = 0
                    self.left_sigueapretada = False
                    if self.right_sigueapretada:
                        self.vx = speed_game
                    else:
                        self.vx = 0
                if event.key == pygame.K_RIGHT:
                    self.vx = 0
                    self.right_sigueapretada = False
                    if self.left_sigueapretada:
                        self.vx = -speed_game
                    else:
                        self.vx = 0
                if event.key == pygame.K_UP:
                    self.vy = 0
                    self.up_sigueapretada = False
                    if self.down_sigueapretada:
                        self.vy = speed_game
                    else:
                        self.vy = -0
                if event.key == pygame.K_DOWN:
                    self.vy = 0
                    self.down_sigueapretada = False
                    if self.up_sigueapretada:
                        self.vy = -speed_game
                    else:
                        self.vy = 0

        self.t += 1

        if self.t > 1:
            self.t = 0

    def on_draw(self, screen):
        if not self.run: return
        self.fondo.draw(screen)
        self.map.draw(screen)
        self.player_1.draw(screen)

        # Part for Server - Dibuja todos los players online que estan en el server.
        if not self.others_players == None:
            for p in self.others_players:
                p.draw(screen)

        # Dibuja todos los moustros que estan en el server.
        if not self.monsters == None:
            for m in self.monsters:
                m.draw(screen)

        if config.QUIT_FLAG == True:  # Termino el juego
            text = self.font.render("GAME OVER", 0, config.COLOR_BLACK)
            screen.blit(text, (100, 240))

    def moving(self):
        self.fondo.update(self.vx, self.vy)
        self.map.update(self.vx, self.vy)
        # self.moving_monster(self.vx, self.vy)

    """ Implementacion para moustros estaticos. """
    def moving_monster(self, vx, vy):
        for m in self.monsters:
            m.update(vx, vy)

    ##############################################
    # PARTE SERVER #
    ##############################################

    """ 1º) Al conectarse un player al Server se ejecuta este metodo automaticamente. """
    def Network_connected(self, data):
        print self.print_sequence(), "Player connected to the server"

    """ 2º) Metodo que se ejecuta cuando se conecta el player al canal del server. """
    def Network_startgame(self, data):
        print self.print_sequence(), "Recibo de Pedido de Login ..."

        self.Send_login(self.nickname, self.password)

    """ 3º) Envio de datos de logueo. """
    def Send_login(self, nickname, password):
        self.Send({"action": "login", "nickname": nickname, "password": password})
        print self.print_sequence(), "Envio de logueo...."

    """ 4º) Metodo de respuesta de logueo. El server va a llamar a este metodo para indicar si el logueo fue exitoso o no. """
    def Network_login(self, data):
        print self.print_sequence(), "Recibo de Logueo ..."

        id = data["id_player"]
        if id == 0: #Logueo Fallado.
            print self.print_sequence(), "Logueo Fallado...."
            exit()
        else:
            self.player_1.id = id
            print self.print_sequence(), "Logueo Exitoso..."

            self.map_number = data["number_map"]

            self.Send({"action": "map", "map": self.map_number})
            print self.print_sequence(), "Pedido de Mapa..."

    """ 5º) Metodo para la creacion del mapa y fondo """
    def Network_map(self, data):
        self.map = map.Map(data["map"], self.map_number)
        self.fondo = fondo.Fondo(config.PATH_BACKS + data["background"])
        print self.print_sequence(), "Recibo de Mapa..."

        # Iniciamos el juego !!!!
        self.run = True
        print self.print_sequence(), "JUEGO INICIADO EXITOSAMENTE ...."

    """ Metodo que actualiza la posicion de los demas players. """
    def Network_updateplayers(self, data):

        id = int(data["id_player"])
        x = int(data["x"])
        y = int(data["y"])
        o = int(data["orientation"])
        t = int(data["t"])

        p = self.get_player(id)
        if p == None: return
        p.server_update(self.fondo.rect.left + x, self.fondo.rect.top + y, o, t)

    """ Obtiene el player pasado como parametro. """
    def get_player(self, id):
        for p in self.others_players:
            if (p.id == id):
                return p


    """ Metodo que se ejecuta cuando se conecta un nuevo player al server. """
    def Network_newplayer(self, data):
        self.others_players.append(player.Player())

    """ N) Al cerrar la conexion con el Server (connection.Close()), se ejecuta este metodo. """
    def Network_disconnected(self, data):
        print self.print_sequence(), "Server disconnected"
        # exit()

    """ Imprime y define las secuencias de ejecucion en el Server. """
    def print_sequence(self):
        self.execute_sequence += 1
        return self.execute_sequence

    """ Crea y añade un nuevo player al juego. """
    def Network_newplayer(self, data):

        id = int(data["id_player"])
        nickname = data["nickname"]
        x = int(data["x"])
        y = int(data["y"])

        p = player.Player(id, nickname)

        self.others_players.append(p)
        p.server_update(self.fondo.rect.left + x, self.fondo.rect.top + y, 0, 0)
        print self.print_sequence(), "Recibiendo y creando informacion de Player: ", nickname

    def Network_newmonster(self, data):

        id = int(data["id_monster"])
        x = int(data["x"])
        y = int(data["y"])

        m = mounstro.Mounstro(id, x, y)

        self.monsters.append(m)

        print self.print_sequence(), "Recibiendo y Creacion informacion de Moustro:", id, "x:", x, "y:", y

    """ Elimina un player que se halla desconectado del server. """
    def Network_delplayer(self, data):
        id = int(data["id_player"])
        find = None

        for p in self.others_players:
            if p.id == id:
                find = p
                break

        pos = self.others_players.index(find)

        del self.others_players[pos]

        print self.print_sequence(), "Player Eliminado: ", find.nickname

    """ Metodo de prueba. """
    def Network_test(self, data):
        list = data["list"]

        for p in list:
            print "Item", p

        print "Lista recibida", list

    def Send_gameoverplayer(self, id_player, current_map):
        self.Send({"action": "delplayer", "id_player": id_player, "map": current_map})
        print "envio de game over ..."

    def next_map(self, map, id_player):
        self.Send({"action": "nextmap", "map": map, "id_player": id_player})
        self.run = False

    def get_monster(self, id):
        for m in self.monsters:
            if (m.id == id):
                return m

    def Network_updatemonters(self, data):
        id = int(data["id_monster"])
        x = int(data["x"])
        y = int(data["y"])
        o = int(data["orientation"])
        t = int(data["t"])

        m = self.get_monster(id)
        if m == None: return
        m.server_update(self.fondo.rect.left + x, self.fondo.rect.top + y, o, t)

