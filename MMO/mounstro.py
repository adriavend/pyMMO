__author__ = 'Adrian'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import config
import threading
import time
import random

class Mounstro(pygame.sprite.Sprite, threading.Thread):
    def __init__(self, x, y):
        threading.Thread.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        #Como hereda de Sprite hay que asignar estos atributos y el metodo update
        self.image_player = pygame.image.load(config.PATH_SPRITES+"monsters.png").convert_alpha()
        self.rect = self.image_player.get_rect()
        self.rect.left, self.rect.top = (x, y)
        self.stop_flag = False

    def is_collision(self, wall):
        for brick in wall:
            if self.rect.colliderect(brick):
                return True
        return False

    #Hereda de Sprite
    def update(self, vx, vy):
        self.rect.move_ip(-vx, -vy)

    def draw(self, screen):
        screen.blit(self.image_player, self.rect)

    #Como hereda de Thread hay que sobreescribir este metodo
    def run(self):
        while self.stop_flag == False:
            for (x, y) in ((0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)):
                self.update(x, y)
                #time.sleep(1)

        #rnd = random.randint(1,4)                      Bachi: probando movimiento aleatorio
        #if rnd == 1:
        #    self.update(-1,0)   #izquierda
        #if rnd == 2:
        #    self.update(1,0)    #derecha
        #if rnd == 1:
        #    self.update(0,1)    #arriba
        #if rnd == 1:
        #    self.update(0,-1)   #abajo

    def stop(self):
        self.stop_flag = True