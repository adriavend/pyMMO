__author__ = 'Adrian'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import config
import threading
import time

class Mounstro(pygame.sprite.Sprite, threading.Thread):
    def __init__(self, x, y):
        threading.Thread.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image_player = pygame.image.load(config.PATH_SPRITES+"monsters.png").convert_alpha()
        self.rect = self.image_player.get_rect()
        self.rect.left, self.rect.top = (x, y)
        self.stop_flag = False

    def is_collision(self, wall):
        for brick in wall:
            if self.rect.colliderect(brick):
                return True
        return False

    def update(self, vx, vy):
        self.rect.move_ip(-vx, -vy)

    def draw(self, screen):
        screen.blit(self.image_player, self.rect)

    def run(self):
        while self.stop_flag == False:
            for (x, y) in ((0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)):
                self.update(x, y)
                #time.sleep(1)

    def stop(self):
        self.stop_flag = True