__author__ = 'Adrian'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import config

class Mounstro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_player = pygame.image.load(config.PATH_SPRITES+"monsters.png").convert_alpha()
        self.rect = self.imagen_player.get_rect()
        self.rect.left, self.rect.top = (x, y)

    def is_collision(self, wall):
        for brick in wall:
            if self.rect.colliderect(brick):
                return True
        return False

    def update(self, vx, vy):
        self.rect.move_ip(-vx, -vy)

    def draw(self, screen):
        screen.blit(self.imagen_player, self.rect)
