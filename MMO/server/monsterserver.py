__author__ = 'Adrian'

import config

"""
    Clase que representa un moustro el cual tiene los datos necesarios para el manejo en el servidor.
"""
class MonsterServer:
    def __init__(self, id, i, j, o, m):
        self.id = id
        self.i = i # Fila en el server.
        self.j = j # Columna en el server.
        self.orientation = o# 1=Derecha, 2=Izquierda, 3=Abajo, 4=Arriba
        self.do_move = m# Movimentos Pendientes a realizar.
        self.is_move = False
        self.t = 0 #Tiempo de movimientos. Cuando se crea obviamente sera 0.

    def x(self):
        return self.j * config.TAB_GAME

    def y(self):
        return self.i * config.TAB_GAME

    def is_complete_mov(self):
        return self.do_move == 0