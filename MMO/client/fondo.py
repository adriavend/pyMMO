import pygame

import config


class Fondo(pygame.sprite.Sprite):
    def __init__(self, path_background):
    	pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path_background).convert_alpha()
        self.rect = self.image.get_rect()
        
    def update(self, vx, vy):
        self.rect.move_ip(-vx, -vy)

    def draw(self, screen):
        screen.fill(config.COLOR_DARKGREEN)
        screen.blit(self.image, self.rect)