__author__ = 'Adrian'

import pygame
import config

class Port(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(config.PATH_SPRITES+"port.gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, vx, vy):
        self.rect.move_ip(-vx, -vy)