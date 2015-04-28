
import time
import sys
import socket
import threading
from thread import start_new_thread

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 6969 # Arbitrary non-privileged port
s = socket.socket()

class ClientConnection():
    def __init__(self):
        pass

    def start(self):
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

        connThread = threading.Thread(target = run, name = "connDaemon")
        connThread.setDaemon(True)
        connThread.start()




def run():
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
        #monster1 = monster.Monster()
        #coor = monster1.posicion()
        #conn.sendall(coor)
        time.sleep(0.2)
        #if not data: 
        #    break
        
        #conn.sendall(reply)
     
    #came out of loop
    print "close"
    conn.close()


