__author__ = 'Bachi'

import pygame


class Boton(pygame.sprite.Sprite):

    def __init__(self, path_image_normal, path_image_select, x=200, y=200):
        self.imagen_normal = pygame.image.load(path_image_normal).convert_alpha()
        self.imagen_seleccionada = pygame.image.load(path_image_select).convert_alpha()
        self.imagen_actual = self.imagen_normal

        self.rect = self.imagen_actual.get_rect()
        self.rect.left, self.rect.top = (x, y)

    def update(self, screen, cursor1):
        if cursor1.colliderect(self.rect):
            self.imagen_actual = self.imagen_seleccionada
        else:
            self.imagen_actual = self.imagen_normal
        screen.blit(self.imagen_actual, self.rect)