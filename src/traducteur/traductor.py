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
        self.length = receivedData[4:6]
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
        self.identSet = set()
        #Load all the device in the base
        for lsensor in sensor.Sensor.objects:
            self.identSet.add(lsensor.physic_id)

    def connect (self, addr, port) :
        self.soc.connect((addr,port))
    
    def receive (self) :
        message = self.soc.recv(1024)
        if message:
            self.trameUsed = trame(message)

    def doChecksum(self,trameUsed):
        """
        Sum up all the bytes of the trame except sep and take the 2 last byte
        """
        sum=0
        sum+=int(trameUsed.length,16)
        sum+=int(trameUsed.rOrg,16)
        sum+=int(trameUsed.data0,16)
        sum+=int(trameUsed.data1,16)
        sum+=int(trameUsed.data2,16)
        sum+=int(trameUsed.data3,16)
        sum+=int(trameUsed.ident[:2],16)
        sum+=int(trameUsed.ident[2:4],16)
        sum+=int(trameUsed.ident[4:6],16)
        sum+=int(trameUsed.ident[6:8],16)
        sum+=int(trameUsed.flag,16)
        sum=hex(sum)
        return sum[(len(sum)-2):].upper()

    def translateTemp(trameUsed):
        """
        return the temperature (range 0-40 c) from data byte 1 
        """
        rowTemp=int(trameUsed.data1,16)
        temp = rowTemp*40/255
        return temp


    def checkTrame(self):
        if ("A55A" not in self.trameUsed.sep):
            logger.info("Wrong separator, rejected")
            return False
        if (self.doChecksum(self.trameUsed) not in self.trameUsed.checkSum):     
            #Mauvais checkSum
            logger.info("Wrong checksum, expected : {}, rejected".format(self.doChecksum()))
            return False
        if (self.trameUsed.ident in self.identSet):
            #Recuperer le capteur en bdd
            sensorUsed = sensor.Sensor.objects(physic_id=self.trameUsed.ident)[0]
            #Identifier le type de trame && Traiter les data de la trame
            newData = '' #la nouvelle data a entrer en base, type dynamique
            if (sensorUsed.__class__.__name__=="Switch"):
                if (self.trameUsed.data3=='09'):
                    logger.info("Door sensor {} with state [close]".format(self.trameUsed.ident))
                    newData = True
                else :
                    logger.info("Door sensor {} with state [open]".format(self.trameUsed.ident))
                    newData = False
            elif (sensorUsed.__class__.__name__=="Temperature"):
                newData = self.translateTemp(self.trameUsed)
                logger.info("Temperature sensor {} with temp {}".format(self.trameUsed.ident, newData))
            else :
                print ko
            "Update de la trame au niveau de la base"
            sensorUsed.update(newData)
            

    def updateIdentSet(self):
        del(self.identSet[:])
        for lsensor in sensor.Sensor.objects:
            self.identSet.add(lsensor.physic_id)



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
    soc.close()
