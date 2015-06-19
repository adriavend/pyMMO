__author__ = 'Adrian'

import pygame
import config

class Heart(pygame.sprite.Sprite):

    def __init__(self):
        self.image = pygame.image.load(config.PATH_SPRITES+"heart.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = (config.MARGIN_SPRITE, config.SCREEN_WIDTH - self.rect.width - config.MARGIN_SPRITE)

    def draw(self, screen):
        screen.blit(self.image, self.rect)