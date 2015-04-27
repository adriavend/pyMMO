__author__ = 'Adrian'

import funciones
import wall
import config
import brick
import port

class Map():

    def __init__(self, file):

        self.list_brick = []
        self.port = None

        self.mapa = funciones.leer_mapa(file)
        self.fil = len(self.mapa)
        self.col = len(self.mapa[0])

        self.tab = config.TAB_GAME

        self.builder_map()
        
    def builder_map(self):
        for f in range(self.fil-1):
            for c in range(self.col):
                x = c*self.tab
                y = f*self.tab
                if self.mapa[f][c] == 'M':
                    self.list_brick.append(brick.Brick(x, y))
                if self.mapa[f][c] == 'P':
                    self.port = port.Port(x, y)

    def draw(self, screen):
        for brick in self.list_brick:
            brick.draw(screen)
        self.port.draw(screen)

    def update(self, vx, vy):
        for brick in self.list_brick:
            brick.update(vx, vy)
        self.port.update(vx, vy)

