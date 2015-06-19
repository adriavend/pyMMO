__author__ = 'Adrian'

import brick, config, treasure, port

import mounstro
import flecha

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

        self.list_flechas = []
        
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
                # elif char == 'M':
                #     self.list_monsters.append(mounstro.Mounstro(x, y))
                elif char == 'T':
                    self.treasure = treasure.Treasure(x, y)

    def draw(self, screen):
        for brick in self.list_brick:
            brick.draw(screen)

        for mons in self.list_monsters:
            mons.draw(screen)

        if not self.port is None:
            self.port.draw(screen)

        if not self.treasure is None:
            self.treasure.draw(screen)

        for f in self.list_flechas:
            f.draw(screen)

    def update(self, vx, vy):
        for brick in self.list_brick:
            brick.update(vx, vy)

        if not self.port is None:
            self.port.update(vx, vy)

        if not self.treasure is None:
            self.treasure.update(vx, vy)

        list_del_flechas_temp = []

        for f in self.list_flechas:
            if f.is_collision_brick(self.list_brick) or f.is_collision_screen():
                list_del_flechas_temp.append(f)
            f.update()

        self.__del_flechas(list_del_flechas_temp)

    def append_monster(self, id, x, y):
        """
        Crea y agrega un nuevo moustro al mapa.
        :param id: Identificador del moustro a crear
        :param x: Posicion x.
        :param y: Posicion y.
        :return: None
        """
        self.list_monsters.append(mounstro.Mounstro(id, x, y))

    def __get_monster(self, id):
        """ Busca y devuelve el moustro pasado como parametro.
        :param id: Identificador del moustro a buscar.
        :return: Objeto moustro encontrado.
        """
        for m in self.list_monsters:
            if (m.id == id):
                return m

    def update_monster(self, id, x, y, o, t):
        """ Actualiza el movimiento de un moustro.
        :param id: Identificador del moustro a actualizar.
        :param x: Posicion x.
        :param y: Posicion y.
        :param o: Orientacion.
        :param t: Tiempo (go=1 o stop=2)
        :return: None
        """
        m = self.__get_monster(id)
        if m is None: return
        m.server_update(x, y, o, t)

    def append_flecha(self, orientation, x, y):
        """ Crea y Agrega una flecha a lista de flechas.
        :param orientation: Orientacion de la flecha.
        :param x: Posicion x de la flecha.
        :param y: Posicion y de la flecha.
        :return: None
        """
        self.list_flechas.append(flecha.Flecha(orientation, x, y))

    def __del_flechas(self, lst_f):
        """ Metodo privado !! Elimina un flecha de la lista.
        :param lst_f: Lista de flechas que tuvieron colision a eliminar.
        :return: None
        """
        for f in lst_f:
            del self.list_flechas[self.list_flechas.index(f)]

    def collide_flecha_player(self, player):
        for f in self.list_flechas:
            if f.rect.colliderect(player.rect):
                del self.list_flechas[self.list_flechas.index(f)]
                player.heart -= 1
