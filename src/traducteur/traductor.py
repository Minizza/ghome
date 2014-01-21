#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Socket very useful to connect to every sh*t in da world"""
import socket

"""I want da base"""
import sys
path = "../Model/Device/"
sys.path.append(path)

from device import *
from sensor import *
from actuator import *
from historic import *

path = "../Model/User/"
sys.path.append(path)

from user import *

from mongoengine import *

connect('test')


class trame :
    """
        La classe trame regroupe toutes les informations qui peuvent être
            récupérées sur une trame, à savoir :
                - sep, le  séparateur de trames should be "A55A"
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

    


class traductor :
    """


    """

    def __init__ (self) :
        for device in Device.objects:
            self.identSet.add(device.physic_id)

    def connect (self, addr, port) :
        soc = socket.socket()
        soc.connect((addr,port))
        while 1 :
            message = soc.recv(1024)
            usedTrame = trame(message)



if __name__ == '__main__':
    soc = socket.socket()
    soc.connect(('',1515))
    while 1 :
        message = soc.recv(1024)
        tram2 = trame(message)
        tram2.nameIt()