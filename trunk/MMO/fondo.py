import pygame
import fondo
import config

class Fondo(pygame.sprite.Sprite):
    def __init__(self):
    	pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load(config.backs+"back_game.gif").convert_alpha()
        self.rect = self.imagen.get_rect()
        
    def update(self, screen, vx, vy):
        self.rect.move_ip(-vx, -vy)
        screen.blit(self.imagen, self.rect)

    def draw(self, screen, vx, vy):
        self.rect.move_ip(-vx, -vy)
        screen.blit(self.imagen, self.rect)