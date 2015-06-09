__author__ = 'Adrian'

import pygame

from client import config


# class Mounstro(pygame.sprite.Sprite,threading.Thread):
class Mounstro(pygame.sprite.Sprite):
    def __init__(self, id, x, y):
        #threading.Thread.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.id = id

        self.image_stop_right = pygame.image.load(config.PATH_SPRITES+"monster_stop_right.png").convert_alpha()
        self.image_go_right = pygame.image.load(config.PATH_SPRITES+"monster_go_right.png").convert_alpha()
        self.image_stop_left = pygame.image.load(config.PATH_SPRITES+"monster_stop_left.png").convert_alpha()
        self.image_go_left = pygame.image.load(config.PATH_SPRITES+"monster_go_left.png").convert_alpha()

        self.image_stop_top = pygame.image.load(config.PATH_SPRITES+"monster_stop_top.png").convert_alpha()
        self.image_go_top = pygame.image.load(config.PATH_SPRITES+"monster_go_top.png").convert_alpha()
        self.image_stop_bottom = pygame.image.load(config.PATH_SPRITES+"monster_stop_bottom.png").convert_alpha()
        self.image_go_bottom = pygame.image.load(config.PATH_SPRITES+"monster_go_bottom.png").convert_alpha()

        self.images = [
            [self.image_stop_right, self.image_go_right],
            [self.image_stop_left, self.image_go_left],
            [self.image_stop_bottom, self.image_go_bottom],
            [self.image_stop_top, self.image_go_top]
        ]

        self.image_current = 0
        self.image = self.images[self.image_current][0]

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (x, y)
        self.stop_flag = config.QUIT_FLAG

    def is_collision(self, wall):
        for brick in wall:
            if self.rect.colliderect(brick):
                return True
        return False

    def update(self, vx, vy):
        self.rect.move_ip(-vx, -vy)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def stop(self):
        self.stop_flag = True

    def server_update(self, x, y, o, t):
        o -=1
        self.image = self.images[o][t]
        self.rect.left = x
        self.rect.top = y