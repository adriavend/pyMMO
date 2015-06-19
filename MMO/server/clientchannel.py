__author__ = 'Adrian'

import PodSixNet.Channel

"""
    Clase que representa un cliente conectado. Representa un canal.. osea un medio para poder enviar y recibir informacion.
"""
class ClientChannel(PodSixNet.Channel.Channel):

    def Network(self, data):
        print data

    """
        Metodo que representa la informacion que envia el cliente al server con la invocacion self.send(data).
        Colocar aca y procesar la informacion quie envia el cliente.
    """
    def Network_updatemoving(self, data):
        map = int(data["map"])
        id = int(data["id_player"])
        x = int(data["x"])
        y = int(data["y"])
        o = int(data["orientation"])
        i = int(data["image"])
        #self._server = MMOServer !!!!
        self._server.updatemoving(map, id, x, y, o, i)

    """ Metodo que recibe los datos de login del player para iniciarse y los envia al servidor. """
    def Network_login(self, data):
        nickname = data["nickname"]
        password = data["password"]

        self._server.login(self, nickname, password)

    """ Metodo que se ejecuta cuando en el cliente llama a 'connection.Close()'. """
    def Close(self):
        self._server.Close_channel(self)

    """ Metodo que el cliente pide el mapa. """
    def Network_map(self, data):
        number_map = int(data["map"])
        self._server.Send_map(self, number_map)

    """ Metodo que el cliente pide los datos del proximo mapa. """
    def Network_nextmap(self, data):
        number_map = int(data["map"])
        id_player = int(data["id_player"])
        self._server.Send_nextmap(number_map, id_player)

    def Network_delplayer(self, data):
        id_player = int(data["id_player"])
        current_map = int(data["map"])
        self._server.Del_player(id_player, current_map)

    def Network_treasurefound(self, data):
        id_player = int(data["id_player"])
        nickname = str(data["nickname_player"])
        #current_map = int(data["map"])
        self._server.Treasure_found(id_player,nickname)
