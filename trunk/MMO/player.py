#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import config
import graphics


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.imagen_player = pygame.image.load("men.png").convert_alpha()
        self.imagen_player = pygame.image.load(config.sprites+"tux.png").convert_alpha()
        self.estaMoviendo = False
        self.orientation = 0
        self.rect = self.imagen_player.get_rect()
        self.rect.top, self.rect.left = (config.SCREEN_HEIGHT / 2, config.SCREEN_WIDTH / 2)


    def is_collision(self, wall):
        return pygame.sprite.collide_rect(self.rect, wall)

    def update(self):
        #screen.blit(self.imagen_player, self.rect)
        pass

    def draw(self, screen):
        screen.blit(self.imagen_player, self.rect)
