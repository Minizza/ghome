#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Socket very useful to connect to every sh*t in da world"""
import socket

"""I want da base"""
from Model.Device import device
from Model.Device import sensor
from Model.Device import switch
from Model.Device import temperature
from Model.Device import actuator
from Model.Device import historic

"""I want da logger"""
import logger.loggerConfig as myLog

from user import *
from mongoengine import *


logger=myLog.configure()
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
        self.data0 = receivedData[8:10]
        self.data1 = receivedData[10:12]
        self.data2 = receivedData[12:14]
        self.data3 = receivedData[14:16]
        self.ident = receivedData[16:24]
        self.flag = receivedData[24:26]
        self.checkSum = receivedData[26:]
    
    def nameIt (self) :
        logger.info("{} is a {} ".format(self.ident,self.rOrg))

    


class traductor :
    """
    TODO écrire la doc

    """

    def __init__ (self) :
        self.soc = socket.socket()
        self.trameUsed = ''
	    """
        Load all the device in the base
        """
        for sensor in Sensor.objects:
            self.identSet.add(device.physic_id)

    def connect (self, addr, port) :
        self.soc.connect((addr,port))
    
    def receive (self) :
        message = self.soc.recv(1024)
        if message:
            self.trameUsed = trame(message)

    def doChecksum(self):
    	"""
        Sum up all the bytes of the trame except sep and take the 2 last byte
        """
        sum=hex(\
            int(self.trameUsed.length,16)+\
            int(self.trameUsed.rOrg,16)+\
            int(self.trameUsed.data0,16)+\
            int(self.trameUsed.data1,16)+\
            int(self.trameUsed.data2,16)+\
            int(self.trameUsed.data3,16)+\
            int(self.trameUsed.ident,16)+\
            int(self.trameUsed.flag,16)\
            )
        return sum[(len(sum)-2):]

    def checkTrame(self):
        if (self.trameUsed.sep=="A55A"):
            logger.info("Wrong separator, rejected")
            return False
        if (self.doChecksum!=self.trameUsed.checkSum):     
        	"Mauvais checkSum"
            logger.info("Wrong checksum, rejected")
        if (self.trameUsed.ident in identSet):
            "Recuperer le capteur en bdd"
            sensorUsed = Sensor.objects(physic_id=self.trameUsed.ident)
            "Identifier le type de trame && Traiter les data de la trame"
            newData = '' #la nouvelle data a entrer en base, type dynamique
            if (sensorUsed.type==Switch):
                if (self.trameUsed.data3=='01'):
                    newData = 'True'
                else :
                    newData = 'False'
            elif (sensorUsed.type==Temperature):
                print okok
            else :
                print ko
            "Update de la trame au niveau de la base"
            sensorUsed.update(newData)



if __name__ == '__main__':
    soc = socket.socket()
    soc.connect(('',1515))
    logger.info("Connection")
    try:
        while 1 :
            message = soc.recv(1024)
            if message:
                tram2 = trame(message)
                tram2.nameIt()
    except socket.error:
        logger.info("Déconnection du serveur")
        soc.close()
    finally:
        soc.close()
