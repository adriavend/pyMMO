#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import scene
import config
import player
import fondo
import wall
import mounstro

class SceneGame(scene.Scene):

     def __init__(self, director):
        scene.Scene.__init__(self, director)

        #Velocidades del Juego
        self.vx, self.vy = (0, 0)

        self.left_sigueapretada, self.right_sigueapretada, self.up_sigueapretada, self.down_sigueapretada = False, False, False, False

        self.fondo_1 = fondo.Fondo(config.BACK_SCENE_GAME)
        self.wall_1 = wall.Wall()
        self.player_1 = player.Player()

        self.mounstro_1 = mounstro.Mounstro(20, 300)
        self.mounstro_1.start()

        # Desactivamos el mouse de la pantalla
        pygame.mouse.set_visible(False)

        self.t = 0

        self.font = pygame.font.Font(None, 92)

     def on_update(self):

         """
         Logica del Juego. Manejo de Movimientos y Colisiones.
         """
         # 1°) Movemos el fondo y las paredes sin importar que halla o no colisiones. Ojo el player no se mueve
         self.moving()

         # 2°) Ahora comprobamos si realmente hay colision entre el player con algun muro.
         # En caso de existir colision -> Movemos en sentido contrario (volviendo a la posicion original que tenia antes)
         if self.player_1.is_collision(self.wall_1.list_block):
             self.fondo_1.update(-self.vx, -self.vy)
             self.wall_1.update(-self.vx, -self.vy)
             self.mounstro_1.update(-self.vx, -self.vy)
         elif self.player_1.is_collision_monsters(self.mounstro_1):
             self.fondo_1.update(-self.vx, -self.vy)
             self.wall_1.update(-self.vx, -self.vy)
             self.mounstro_1.update(-self.vx, -self.vy)
             self.player_1.change_image_explosion()
             self.mounstro_1.stop()
             config.QUIT_FLAG = True
         else:
             # 3°) Ahora comprobamos que si el fondo se mueve saliendose de la pantalla entonces que se empieze a mover el player
             if self.fondo_1.rect.left > 0 \
                     or self.fondo_1.rect.right < config.SCREEN_WIDTH \
                     or self.fondo_1.rect.top > 0 \
                     or self.fondo_1.rect.bottom < config.SCREEN_HEIGHT: # Si el fondo se quiere desprender de la izquierda de la pantalla or de la derecha o arriba o abajo.
                 self.fondo_1.update(-self.vx, -self.vy)  #No se mueve. Regrega una direccion
                 self.wall_1.update(-self.vx, -self.vy) # No se mueve. Regrega una direccion
                 self.mounstro_1.update(-self.vx, -self.vy)
                 self.player_1.update(self.vx, self.vy, self.t) # Se mueve. Porque nunca le indicamos que se moviera
             else:
                 self.player_1.update(self.vx/2, self.vy/2, self.t) # self.vx/2 reduce la velocidad a la mitad para que puede ir al medio de la pantalla.

             # Controlamos que el player no se salga de la pantalla. Caso contrario volvemos una direccion
             if self.player_1.rect.left == 0 \
                     or self.player_1.rect.right > config.SCREEN_WIDTH\
                     or self.player_1.rect.top == 0 \
                     or self.player_1.rect.bottom > config.SCREEN_HEIGHT:
                self.player_1.update(-self.vx, -self.vy, self.t)
         #---------------------------------------------------------------------------------------------------------

     def on_event(self, events):
        speed_game = config.SPEED_GAME

        for event in events:
            if event.type == pygame.QUIT:
                self.mounstro_1.stop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left_sigueapretada = True
                    self.vx =- speed_game
                if event.key == pygame.K_RIGHT:
                    self.right_sigueapretada = True
                    self.vx = speed_game
                if event.key == pygame.K_UP:
                    self.up_sigueapretada = True
                    self.vy =- speed_game
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
                         self.vx =-speed_game
                     else:
                         self.vx = 0
                if event.key == pygame.K_UP:
                    self.vy = 0
                    self.up_sigueapretada = False
                    if self.down_sigueapretada:
                        self.vy = speed_game
                    else:
                        self.vy=-0
                if event.key == pygame.K_DOWN:
                    self.vy = 0
                    self.down_sigueapretada=False
                    if self.up_sigueapretada:
                        self.vy=-speed_game
                    else:
                        self.vy=0

        self.t +=1

        if self.t > 1:
            self.t = 0

     def on_draw(self, screen):
        self.fondo_1.draw(screen)
        self.wall_1.draw(screen)
        self.player_1.draw(screen)
        self.mounstro_1.draw(screen)

        if config.QUIT_FLAG == True: # Termino el juego
            text = self.font.render("GAME OVER", 0, config.COLOR_BLACK)
            screen.blit(text, (100, 240))

     def moving(self):
         self.fondo_1.update(self.vx, self.vy)
         self.wall_1.update(self.vx, self.vy)
         self.mounstro_1.update(self.vx, self.vy)