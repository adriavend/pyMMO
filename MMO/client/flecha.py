__author__ = 'Adrian'

import pygame
import config

class Flecha(pygame.sprite.Sprite):

    def __init__(self, orientation, x, y):
        """ Constructor de la clase.
        """
        pygame.sprite.Sprite.__init__(self)
        self.rect = None

        if orientation == 1:
            self.rect = pygame.Rect(x + config.MARGIN_SPRITE, y, config.FLECHA_WIDTH, config.FLECHA_HEIGTH)
        elif orientation == 2:
            self.rect = pygame.Rect(x - config.MARGIN_SPRITE - config.FLECHA_WIDTH, y, config.FLECHA_WIDTH,
                                    config.FLECHA_HEIGTH)
        elif orientation == 3:
            self.rect = pygame.Rect(x, y + config.MARGIN_SPRITE, config.FLECHA_HEIGTH, config.FLECHA_WIDTH)
        elif orientation == 4:
            self.rect = pygame.Rect(x, y - config.MARGIN_SPRITE - config.FLECHA_WIDTH, config.FLECHA_HEIGTH,
                                    config.FLECHA_WIDTH)

        self.orientation = orientation

    def draw(self, screen):
        """ Metodo que dibuja el componente en la pantalla pasada como parametro.
        :param screen: Pantalla en donde dibujarlo.
        :return: None
        """
        pygame.draw.rect(screen, config.COLOR_YELLOW, self.rect, 0)

    def update(self):
        """ Metodo que actualiza el componente (toma algun accion de acuerdo a sus variables).
        :return: None
        """
        if not self.rect is None:
            if self.orientation == 1:
                self.rect.move_ip(config.SPEED_GAME, 0)
            elif self.orientation == 2:
                self.rect.move_ip(-config.SPEED_GAME, 0)
            elif self.orientation == 3:
                self.rect.move_ip(0, config.SPEED_GAME)
            elif self.orientation == 4:
                self.rect.move_ip(0, -config.SPEED_GAME)

    def is_collision_brick(self, bricks):
        """ Verifica si existen colisiones con los bloques pasados como parametro.
        :param bricks: Lista de bloques.
        :return: True si hay colision. False caso contrario.
        """
        for brick in bricks:
            if self.rect.colliderect(brick.rect):
                return True
        return False

    def is_collision_monsters(self, monsters):
        """ Verifica si existen colisiones con los moustros pasados como parametro.
        :param monsters: Lista de moustros
        :return: True si hay colision. False caso contrario.
        """
        for monster in monsters:
            if self.rect.colliderect(monster.rect):
                return True
        return False

    def is_collision_screen(self):
        """ Verifica si la flecha se ha salido de la pantalla.
        :return: True si se ha salido. False caso contrario.
        """
        if self.rect.right > config.SCREEN_WIDTH or \
            self.rect.bottom > config.SCREEN_HEIGHT or \
            self.rect.left < 0 or \
            self.rect.top < 0:
            return True
        return False

