
import socket

class Cliente():
    def __init__(self):
        self.soc = socket.socket()
        self.soc.connect(("localhost", 6969))

    def send(self,frulandi):
       self.soc.send(frulandi)

    def recv(self):
       return self.soc.recv(1000)

    def close(self):
    # Cerramos el socket
        self.soc.close()

