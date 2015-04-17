__author__ = 'Bachi'

import pygame


class Boton(pygame.sprite.Sprite):

    def __init__(self, pathImagenNormal, pathImagenSeleccionada, x=200, y=200):
        self.imagen_normal = pygame.image.load(pathImagenNormal).convert_alpha()
        self.imagen_seleccionada = pygame.image.load(pathImagenSeleccionada).convert_alpha()
        self.imagen_actual = self.imagen_normal

        self.rect = self.imagen_actual.get_rect()
        self.rect.left, self.rect.top = (x, y)

    def update(self, pantalla, cursor1):
        if cursor1.colliderect(self.rect):
            self.imagen_actual = self.imagen_seleccionada
        else:
            self.imagen_actual = self.imagen_normal

        pantalla.blit(self.imagen_actual, self.rect)


    def draw(self, screen):
        screen.blit(self.imagen_normal, self.rect)