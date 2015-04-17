__author__ = 'Bachi'

import pygame

class Boton(pygame.sprite.Sprite):

    def __init__(self, imagen1, imagen2, x=200, y=200):
        self.imagen_normal = imagen1
        self.imagen_seleccionada = imagen2
        self.imagen_actual = self.imagen_normal
        self.rect = self.imagen_actual.get_rect()
        self.rect.left, self.rect.top = (x, y)

    def update(self, pantalla, cursor):
        if cursor.colliderect(self.rect):
            self.imagen_actual = self.imagen_seleccionada
        else:
            self.imagen_actual = self.imagen_normal

        pantalla.blit(self.imagen_actual, self.rect)

