# -*- coding: utf-8 -*-
import socket
import thread
import atexit


"""
Multi threaded echo to everyone
"""
clientList=[]
def handler(clientsock,addr):
       while 1:
            data = clientsock.recv(BUFSIZ)
            if not data: break
            print "Broadcasted data : {}".format(data)
            for client in clientList:
                client.send(data)
       clientsock.close()


if __name__=='__main__':
        HOST = 'localhost'
        PORT = 1515
        BUFSIZ = 1024
        ADDR = (HOST, PORT)
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversock.bind(ADDR)
        serversock.listen(10)

        while 1:
            print 'waiting for connection…'
            clientsock, addr = serversock.accept()
            clientList.append(clientsock)
            print '…connected from:', addr
            thread.start_new_thread(handler, (clientsock, addr))
#some other cleanup code if necessary
