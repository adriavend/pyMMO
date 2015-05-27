#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import scene
import config
import player
import fondo
import mounstro
import map

from PodSixNet.Connection import ConnectionListener, connection
from time import sleep


class SceneGame(scene.Scene, ConnectionListener):
    def __init__(self, director):
        scene.Scene.__init__(self, director)

        # Velocidades del Juego
        self.vx, self.vy = (0, 0)

        self.left_sigueapretada, self.right_sigueapretada, self.up_sigueapretada, self.down_sigueapretada = False, False, False, False

        self.fondo_1 = fondo.Fondo(config.BACK_SCENE_GAME)

        self.map = map.Map(config.PATH_MAPS + "map_1.txt")

        self.player_1 = player.Player()

        self.list_players = []

        self.mounstro_1 = mounstro.Mounstro(20, 300)
        #self.mounstro_1.start()

        # Desactivamos el mouse de la pantalla
        pygame.mouse.set_visible(False)

        self.t = 0

        self.font = pygame.font.Font(None, 92)

        #<Server>
        self.Connect()
        # #</Server>

        self.running = False

        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.01)


    def on_update(self):
        # <Server>
        connection.Pump()
        self.Pump()  # llama a Network_startgame()
        #</Server>

        # self.serverUpdate()
        # self.cliente.refreshPlayerPosition(self.player_1.getPosition())
        """
         Logica del Juego. Manejo de Movimientos y Colisiones.
         """
        # 1°) Movemos el fondo y las paredes sin importar que halla o no colisiones. Ojo el player no se mueve
        self.moving()

        # 2°) Ahora comprobamos si realmente hay colision entre el player con algun muro.
        # En caso de existir colision -> Movemos en sentido contrario (volviendo a la posicion original que tenia antes)
        if self.player_1.is_collision(self.map.list_brick):
            self.fondo_1.update(-self.vx, -self.vy)
            self.map.update(-self.vx, -self.vy)
            self.mounstro_1.update(-self.vx, -self.vy)
        elif self.player_1.is_collision_monsters(self.mounstro_1):
            self.fondo_1.update(-self.vx, -self.vy)
            self.map.update(-self.vx, -self.vy)
            self.mounstro_1.update(-self.vx, -self.vy)
            self.player_1.change_image_explosion()
            self.mounstro_1.stop()
            config.QUIT_FLAG = True
        else:
            # 3°) Ahora comprobamos que si el fondo se mueve saliendose de la pantalla entonces que se empieze a mover el player
            if self.fondo_1.rect.left > 0 \
                    or self.fondo_1.rect.right < config.SCREEN_WIDTH \
                    or self.fondo_1.rect.top > 0 \
                    or self.fondo_1.rect.bottom < config.SCREEN_HEIGHT:  # Si el fondo se quiere desprender de la izquierda de la pantalla or de la derecha o arriba o abajo.
                self.fondo_1.update(-self.vx, -self.vy)  #No se mueve. Regrega una direccion
                self.map.update(-self.vx, -self.vy)  # No se mueve. Regrega una direccion
                self.mounstro_1.update(-self.vx, -self.vy)
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

        # Si existe movimiento ... entonces mandamos las coordenas la servidor.
        # if not (self.vx, self.vy) == (0, 0):
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
        x = abs(self.fondo_1.rect.left) + self.player_1.rect.left
        y = abs(self.fondo_1.rect.top) + self.player_1.rect.top
        self.Send({"action": "place", "x": x, "y": y,
                   "id_player": self.player_1.id})
        sleep(0.01)

    def on_event(self, events):
        speed_game = config.SPEED_GAME

        for event in events:
            if event.type == pygame.QUIT:
                self.stop()
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
        self.fondo_1.draw(screen)
        self.map.draw(screen)
        self.player_1.draw(screen)
        self.mounstro_1.draw(screen)

        if config.QUIT_FLAG == True:  # Termino el juego
            text = self.font.render("GAME OVER", 0, config.COLOR_BLACK)
            screen.blit(text, (100, 240))

        # Part for Server - Dibuja todos los players online que estan en el server.
        if not self.list_players == None:
            for p in self.list_players:
                p.draw(screen)

    def moving(self):
        self.fondo_1.update(self.vx, self.vy)
        self.map.update(self.vx, self.vy)
        self.mounstro_1.update(self.vx, self.vy)

    def stop(self):
        self.mounstro_1.stop()

    ##############################################
    # PARTE SERVER #
    ##############################################
    """
        Metodo que se ejecuta cuando se conecta el cliente al server.
     """

    def Network_startgame(self, data):
        self.running = True

        cant_players_online = int(data["players"])

        for i in range(cant_players_online):
            self.list_players.append(player.Player())

        self.player_1.id = int(data["id_player"])

    def Network_place(self, data):
        id = int(data["id_player"])
        p = self.list_players[id - 2]
        p.server_update(self.fondo_1.rect.left + int(data["x"]), self.fondo_1.rect.top + int(data["y"]))

    """
        Metodo que se ejecuta cuando se conecta un nuevo player al server.
    """
    def Network_newplayer(self, data):
        self.list_players.append(player.Player())
