__author__ = 'Adrian'

import pygame
import config
import graphics
import funciones


class Wall(pygame.sprite.Sprite):
    def __init__(self, archivo):
        pygame.sprite.Sprite.__init__(self)
        self.list_block = []

        self.mapa = funciones.leer_mapa(archivo)
        self.fil = len(self.mapa)
        self.col = len(self.mapa[0])

        self.size = config.BLOCK_SIZE
        self.tab = config.TAB_GAME

        self.append_block()

        # self.list_block.append(pygame.Rect(400, 50, config.BLOCK_WIDTH, 120))
        # self.list_block.append(pygame.Rect(150, 350, 200, config.BLOCK_HEIGHT))
        # self.list_block.append(pygame.Rect(800, 150, config.BLOCK_WIDTH, 150))

    def update(self, vx, vy):
        for block in self.list_block:
            block.move_ip(-vx, -vy)

    def draw(self, screen):
        for block in self.list_block:
            pygame.draw.rect(screen, config.COLOR_NARROW, block)

    def append_block(self):
        for f in range(self.fil-1):
            for c in range(self.col):
                if self.mapa[f][c] == 'M':
                    self.list_block.append(pygame.Rect(c*self.tab, f*self.tab, self.size, self.size))

