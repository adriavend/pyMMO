import pygame
import fondo
import config

class Fondo(pygame.sprite.Sprite):
    def __init__(self):
    	pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load(config.backs+"back_game.gif").convert_alpha()
        self.rect = self.imagen.get_rect()
        
    def update(self, vx, vy):
        self.rect.move_ip(-vx, -vy)

    def draw(self, screen):
        screen.fill(config.COLOR_DARKGREEN)
        screen.blit(self.imagen, self.rect)