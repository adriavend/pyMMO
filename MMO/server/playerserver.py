__author__ = 'Adrian'

"""
    Clase que representa un cliente el cual tiene los datos necesarios para el manejo en el servidor.
"""
class PlayerServer:
    def __init__(self, id):
        self.id = id
        self.channel = None
        self.pos_x = 0
        self.pos_y = 0
        self.map = 1
        self.nickname = ""
        self.password = ""
        self.t = 0
        self.orientation = 0
