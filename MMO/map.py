__author__ = 'Adrian'

import config
import brick
import port
import mounstro
import treasure

class Map():

    def __init__(self, mapa, number):
        self.mapa = mapa
        self.fil = len(self.mapa)
        self.col = len(self.mapa[0])

        self.list_brick = []
        self.list_monsters = []
        self.port = None
        self.treasure = None

        self.tab = config.TAB_GAME

        self.n = number
        self.builder_map()
        
    def builder_map(self):
        for f in range(self.fil-1):
            for c in range(self.col):
                x = c*self.tab
                y = f*self.tab
                char = self.mapa[f][c]
                if char == 'B':
                    self.list_brick.append(brick.Brick(x, y, self.n))
                elif char == 'P':
                    self.port = port.Port(x, y)
                elif char == 'M':
                    self.list_monsters.append(mounstro.Mounstro(x, y))
                elif char == 'T':
                    self.treasure = treasure.Treasure(x, y)

    def draw(self, screen):
        for brick in self.list_brick:
            brick.draw(screen)

        for mous in self.list_monsters:
            mous.draw(screen)

        if not self.port is None:
            self.port.draw(screen)

        if not self.treasure is None:
            self.treasure.draw(screen)

    def update(self, vx, vy):
        for brick in self.list_brick:
            brick.update(vx, vy)

        for mous in self.list_monsters:
            mous.update(vx, vy)

        if not self.port is None:
            self.port.update(vx, vy)

        if not self.treasure is None:
            self.treasure.update(vx, vy)

