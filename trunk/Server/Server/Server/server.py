## coding=utf-8
#from __future__ import print_function

#__author__ = 'Bachi'

#import socket

#def main():

#    # Creamos el socket.
#    server = socket.socket()

#    # Conecta el socket con la direccion.
#    server.bind(("localhost", 6969))

#    # Empieza a escuchar conexiones.
#    server.listen(1)

#    # Aceptamos una conexion, se bloquea hasta que alguien se conecte.
#    print("Esperando conexion...")
#    socket_cliente, datos_cliente = server.accept()
#    # Imprime la información del cliente conectado.
#    print("Conectado con: " + datos_cliente[0] + ":" + str(datos_cliente[1]))

#    while 1:
#        print("Esperando mensaje...")
#        # Esperamos que el cliente mande un mensaje y lo imprimimos.
#        datos = socket_cliente.recv(1000)   #1000 = bufsize
#        datos = datos.decode('utf-8')
#        print ("El mensaje es:", datos)
#        # Si el mensaje es "quit" se termina el bucle.
#        if datos == "quit":
#            #socket_cliente.send("chau")
#            break

#    print("Cerrando...")
#    # Cerramos ambos sockets.
#    socket_cliente.close()
#    server.close()

#if __name__ == "__main__":
#    main()

##---------------------------------------------------------------------------------------------------------------------

import time
import monster
import socket
import sys
from thread import *
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 6969 # Arbitrary non-privileged port
 
def main():
    print 'Generando mundo'


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'
 
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
     
    print 'Socket bind complete'
 
#Start listening on socket
    s.listen(10)
    print 'Socket now listening'
 
    #now keep talking with the client
    while 1:
    #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(clientthread,(conn,))
 
    s.close()


#Function for handling connections. This will be used to create threads
def clientthread(conn):
   
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        #reply = 'OK...' + data
        monster1 = monster.Monster()
        coor = monster1.posicion()
        conn.sendall(coor)
        time.sleep(0.2)
        #if not data: 
        #    break
        
        #conn.sendall(reply)
     
    #came out of loop
    print "close"
    conn.close()


if __name__ == "__main__":
    main()


def generarMundo():
    return monster.Monster()