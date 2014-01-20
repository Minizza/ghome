#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket

"""
#st="A55A0B06000000080001B25E002A"
#st="0"
#print(' '.join(format(x, 'b') for x in bytearray(st)))
my_hexdata = "A55A0B05000000000021CBE320FF"
scale = 16 ## equals to hexadecimalœ
num_of_bits = len(my_hexdata)*4
print(bin(int(my_hexdata, scale))[2:].zfill(num_of_bits))
"""



class trame :
    """
        La classe trame regroupe toutes les informations qui peuvent être récupérées sur une
            trame, à savoir : 
                - sep, le  séparateur de trames
                - lenght, la longueur des infos d'une trame
                - rOrg, le type de trame
                - dataX, le byte de data X
                - ident, l'identifiant physique du capteur
                - flag , ...
                - checkSum, ...
    """
    def __init__ (self,receivedData) :
        self.sep = receivedData[:4]
        self.lenght = receivedData[4:6]
        self.rOrg = receivedData[6:8]
        self.data1 = receivedData[8:10]
        self.data2 = receivedData[10:12]
        self.data3 = receivedData[12:14]
        self.data4 = receivedData[14:16]
        self.ident = receivedData[16:24]
        self.flag = receivedData[24:26]
        self.checkSum = receivedData[26:]
    
    def nameIt (self) :
        name = ''
        name += self.ident
        name += ' is a '
        name += self.rOrg 
        print name

def main () :
    soc = socket.socket()
    soc.connect(('',1515))
    while 1 :
        message = soc.recv(1024)
        tram2 = trame(message)
        tram2.nameIt()


main()

