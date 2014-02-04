#!/usr/bin/python 
# -*-coding:Utf-8 -*

import socket
import sys
import time
import atexit
from thread import *
from random import randrange

"""I want da logger"""
import logger.loggerConfig as myLog

logger=myLog.configure()


def balTemp (c):
    data = 'A55A0B06000000080001B25E002A'
    print "Sending : {}".format(data)
    c.send(data)

def balCont (c):
    data = 'A55A0B07A830000F00053F440081'
    print "Sending : {}".format(data)
    c.send(data)

def balPres (c):
    data = 'A55A0B079DB8000D0004E59500F2'
    print "Sending : {}".format(data)
    c.send(data)

def clientthread(conn,jeromeIn):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        if data:
            print "reçu d'un user : {}".format(data)
            reply = data
            conn.sendall(reply)

        tramesfromJerome = jeromeIn.recv(1024)
        if tramesfromJerome:
            print "recu de gérome : {}".format(tramesfromJerome)
            conn.sendall(tramesfromJerome)

    #came out of loop
    conn.close()

if __name__ == '__main__':

    OUT_HOST = ''   # Symbolic name meaning all available interfaces
    OUT_PORT = 8888 # Arbitrary non-privileged port

    #Gérome !
    IN_HOST = '134.214.106.23'  
    IN_PORT = 5000



    passOut = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'
    #Bind socket to local host and port
    try:
        passOut.bind((OUT_HOST, OUT_PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()    
    print 'Socket bind complete'
    #Start listening on socket
    passOut.listen(10)
    print 'Socket now listening'


    passIn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    passIn.connect((IN_HOST,IN_PORT))
    print " passerelle trop fat démarrée !"


    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = passOut.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
         
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(clientthread ,(conn,passIn))