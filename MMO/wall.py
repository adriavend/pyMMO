__author__ = 'Adrian'

import pygame
import config
import graphics


class Wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.list_block = []
        self.list_block.append(pygame.Rect(400, 50, config.BLOCK_WIDTH, 200))
        # self.list_block.append(pygame.Rect(400, 70, config.BLOCK_WIDTH, config.BLOCK_HEIGHT))
        # self.list_block.append(pygame.Rect(400, 90, config.BLOCK_WIDTH, config.BLOCK_HEIGHT))
        # self.list_block.append(pygame.Rect(400, 110, config.BLOCK_WIDTH, config.BLOCK_HEIGHT))
        # self.list_block.append(pygame.Rect(400, 130, config.BLOCK_WIDTH, config.BLOCK_HEIGHT))
        # self.list_block.append(pygame.Rect(400, 150, config.BLOCK_WIDTH, config.BLOCK_HEIGHT))

        self.list_block.append(pygame.Rect(800, 150, config.BLOCK_WIDTH, config.BLOCK_HEIGHT))

    def update(self):
        pass

    def draw(self, screen, vx, vy):
        for block in self.list_block:
            pygame.draw.rect(screen, config.COLOR_NARROW, block)
            block.move_ip(-vx, -vy)
