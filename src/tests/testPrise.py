# -*- coding: utf-8 -*-

from traducteur import trame
import socket

def main():                               
    myTrame = trame.trame("A55A6B0550000000FF9F1E0730")
    # myTrame = trame.trame("A55A0B05700000000021CBE330")
    myTrame.calculateChecksum()
    print "trame envoyé : {}".format(myTrame.rawView())
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.connect(('134.214.106.23', 5000))
    server.send(myTrame.rawView())

if __name__ == '__main__':
    main()