#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import scene
import config
import player
import fondo
import wall

class SceneGame(scene.Scene):
     """Escena inicial del juego, esta es la primera que se carga cuando inicia"""
     def __init__(self, director):
        scene.Scene.__init__(self, director)

        #Velocidades del Juego
        self.vx = 0
        self.vy = 0

        self.left_sigue_apretada, self.right_sigueapretada, self.up_sigueapretada, self.down_sigueapretada = False, False, False, False

        self.fondo_1 = fondo.Fondo(config.BACK_SCENE_GAME)
        self.wall_1 = wall.Wall()
        self.player_1 = player.Player()
        self.caption = "MMO"

        self.collision = False

     def on_update(self):

         """
         Logica del Juego.
         Manejo de Movimientos y Colisiones.
         """
         # 1°) Movemos el fondo y las paredes sin importar que halla o no colisiones. Ojo el player no se mueve
         self.fondo_1.update(self.vx, self.vy)
         self.wall_1.update(self.vx, self.vy)

         # 2°) Ahora comprobamos si realmente hay colision entre el player con algun muro.
         # En caso de existir colision -> Movemos en sentido contrario (volviendo a la posicion original que tenia antes)
         if self.player_1.is_collision(self.wall_1.list_block):
             self.fondo_1.update(-self.vx, -self.vy)
             self.wall_1.update(-self.vx, -self.vy)
         else:
             # 3°) Ahora comprobamos que si el fondo se mueve saliendose de la pantalla entonces que se empieze a mover el player
             if self.fondo_1.rect.left > 0:
                 self.fondo_1.update(-self.vx, -self.vy)  #No se mueve. Regrega una direccion
                 self.wall_1.update(-self.vx, -self.vy) # No se mueve. Regrega una direccion
                 self.player_1.update(-self.vx, -self.vy) # Se mueve. Porque nunca le indicamos que se moviera
             if self.player_1.rect.centerx < config.SCREEN_WIDTH /2:
                 self.fondo_1.update(-self.vx, -self.vy)  # Se mueve. Regrega una direccion
                 self.wall_1.update(-self.vx, -self.vy) # Se mueve. Regrega una direccion
                 self.player_1.update(-self.vx, -self.vy) # No Se mueve. Porque nunca le indicamos que se moviera
             if self.player_1.rect.centerx > self.fondo_1.rect.right/2:
                 self.fondo_1.update(-self.vx, -self.vy)
                 self.wall_1.update(-self.vx, -self.vy)
                 self.player_1.update(-self.vx, -self.vy)


             if self.fondo_1.rect.right < config.SCREEN_WIDTH:
                 self.fondo_1.update(-self.vx, -self.vy)
                 self.wall_1.update(-self.vx, -self.vy)
                 self.player_1.update(-self.vx, -self.vy)

             # Controlo que el player no se salga
             if self.player_1.rect.left == 0:
                 self.player_1.update(self.vx, self.vy)
             if self.player_1.rect.right == config.SCREEN_WIDTH:
                 self.player_1.update(self.vx, self.vy)



     def on_event(self, events):
        #pass
        speed_game = config.SPEED_GAME

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    #self.left_sigueapretada = True
                    self.vx =- speed_game
                if event.key == pygame.K_RIGHT:
                    #self.right_sigueapretada = True
                    self.vx = speed_game
                if event.key == pygame.K_UP:
                    #self.up_sigueapretada = True
                    self.vy =- speed_game
                if event.key == pygame.K_DOWN:
                    #self.down_sigueapretada = True
                    self.vy = speed_game

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.vx = 0
                    # self.left_sigueapretada = False
                    # if self.right_sigueapretada:
                    #     vx = speed_game
                    # else:
                    #     vx = 0
                if event.key == pygame.K_RIGHT:
                    self.vx = 0
                    # self.right_sigueapretada = False
                    # if self.left_sigueapretada:
                    #     vx =-speed_game
                    # else:
                    #     vx = 0
                if event.key == pygame.K_UP:
                    self.vy = 0
                    # self.up_sigueapretada = False
                    # if self.down_sigueapretada:
                    #     vy = speed_game
                    # else:vy=-0
                if event.key == pygame.K_DOWN:
                    self.vy = 0
                    # self.down_sigueapretada=False
                    # if self.up_sigueapretada:
                    #     vy=-speed_game
                    # else:
                    #     vy=0

     def on_draw(self, screen):
        self.fondo_1.draw(screen)
        self.wall_1.draw(screen)
        self.player_1.draw(screen)
        #pass

     def moving(self):
         self.fondo_1.update(-self.vx, -self.vy)
         self.wall_1.update(-self.vx, -self.vy)
         self.player_1.update(-self.vx, -self.vy)