import pygame

from client import config


class Brick(pygame.sprite.Sprite):

    def __init__(self, x, y, n):
        pygame.sprite.Sprite.__init__(self)
        path = "%sbrick_%s.png" % (config.PATH_SPRITES, n)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, vx, vy):
        self.rect.move_ip(-vx, -vy)
