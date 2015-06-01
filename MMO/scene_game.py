#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import scene
import config
import player
import fondo
import map
import sys

from PodSixNet.Connection import ConnectionListener, connection
from time import sleep

class SceneGame(scene.Scene, ConnectionListener):
    def __init__(self, director, nickname, password):
        scene.Scene.__init__(self, director)

        pygame.mouse.set_visible(False)

        # Velocidades del Juego
        self.vx, self.vy = (0, 0)

        self.left_sigueapretada, self.right_sigueapretada, self.up_sigueapretada, self.down_sigueapretada = False, False, False, False

        self.fondo = fondo.Fondo(config.PATH_BACKS + "none.gif")
        self.map_number = 1
        self.map = None#map.Map(config.PATH_MAPS + "map_1.txt")
        self.player_1 = player.Player(0, nickname)
        self.others_players = []

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
        if self.player_1.is_collision(self.map.list_brick):
            self.fondo.update(-self.vx, -self.vy)
            self.map.update(-self.vx, -self.vy)
        elif self.player_1.is_collision_monsters(self.map.list_monsters):
            self.fondo.update(-self.vx, -self.vy)
            self.map.update(-self.vx, -self.vy)
            self.player_1.change_image_explosion()
            config.QUIT_FLAG = True
            """
                Envia la señal de desconexion al server para que nos borre del mismo.
                Esto se procesara en el metedo Close() de ClientChannel.
            """
            connection.Close()
            print self.print_sequence(), "Desconetado del Server..."
        else:
            # 3°) Ahora comprobamos que si el fondo se mueve saliendose de la pantalla entonces que se empieze a mover el player
            if self.fondo.rect.left > 0 \
                    or self.fondo.rect.right < config.SCREEN_WIDTH \
                    or self.fondo.rect.top > 0 \
                    or self.fondo.rect.bottom < config.SCREEN_HEIGHT:  # Si el fondo se quiere desprender de la izquierda de la pantalla or de la derecha o arriba o abajo.
                self.fondo.update(-self.vx, -self.vy)  #No se mueve. Regrega una direccion
                self.map.update(-self.vx, -self.vy)  # No se mueve. Regrega una direccion
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

            # Obtenemos la orientacion ... osea.. hacia donde mira... a la izquierda .. o derecha.
            orientation = 0
            if self.vx > 0: orientation = 0
            elif self.vx < 0: orientation = 1

            self.Send({"action": "updatemoving", "x": x, "y": y, "id_player": self.player_1.id, "orientation": orientation, "t": self.t})
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

        if config.QUIT_FLAG == True:  # Termino el juego
            text = self.font.render("GAME OVER", 0, config.COLOR_BLACK)
            screen.blit(text, (100, 240))

        # Part for Server - Dibuja todos los players online que estan en el server.
        if not self.others_players == None:
            for p in self.others_players:
                p.draw(screen)

    def moving(self):
        self.fondo.update(self.vx, self.vy)
        self.map.update(self.vx, self.vy)

    ##############################################
    # PARTE SERVER #
    ##############################################

    """ Metodo que actualiza la posicion de los demas players. """
    def Network_updateplayers(self, data):

        id = int(data["id_player"])
        x = int(data["x"])
        y = int(data["y"])
        o = int(data["orientation"])
        t = int(data["t"])

        p = self.get_player(id)
        p.server_update(self.fondo.rect.left + x, self.fondo.rect.top + y, o, t)

    """ Obtiene el player pasado como parametro. """
    def get_player(self, id):
        for p in self.others_players:
            if (p.id == id):
                return p

    """ Metodo que se ejecuta cuando se conecta un nuevo player al server. """
    def Network_newplayer(self, data):
        self.others_players.append(player.Player())

    """ 2º) Metodo que se ejecuta cuando se conecta el player al canal del server. """
    def Network_channel(self, data):
        self.player_1.str_channel = data["channel"]
        print self.print_sequence(), "Recibo de canal ..."

        self.Send_login(self.nickname, self.password)

    """ 3º) Envio de datos de logueo. """
    def Send_login(self, nickname, password):
        self.Send({"action": "login", "channel": self.player_1.str_channel, "nickname": nickname, "password": password})
        print self.print_sequence(), "Envio de logueo...."

    """
        4º) Metodo de respuesta de logueo. El server va a llamar a este metodo para indicar si el logueo fue exitoso o no.
    """
    def Network_login(self, data):

        print self.print_sequence(), "Recibo de Logueo ..."

        id = data["id_player"]

        if id == 0: #Logueo Fallado.
            print self.print_sequence(), "Logueo Fallado...."
            exit()
        else:
            self.player_1.id = id
            print self.print_sequence(), "Logueo Exitoso..."

            self.Send({"action": "map"})
            print self.print_sequence(), "Pedido de Mapa..."

    """ N) Al cerrar la conexion con el Server (connection.Close()), se ejecuta este metodo. """
    def Network_disconnected(self, data):
        print self.print_sequence(), "Server disconnected"
        # exit()

    """ 1º) Al conectarse un player al Server se ejecuta este metodo automaticamente. """
    def Network_connected(self, data):
        print self.print_sequence(), "Player connected to the server"

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

        print self.print_sequence(), "Player desconectado: ", find.nickname

    """ Metodo de prueba. """
    def Network_test(self, data):
        list = data["list"]

        for p in list:
            print "Item", p

        print "Lista recibida", list

    """ Metodo para la creacion del mapa y fondo """
    def Network_map(self, data):
        self.map = map.Map(data["map"])
        self.fondo = fondo.Fondo(config.PATH_BACKS + data["background"])
        print self.print_sequence(), "Recibo de Mapa..."

        # Iniciamos el juego !!!!
        self.run = True
        print self.print_sequence(), "JUEGO INICIADO EXITOSAMENTE ...."
