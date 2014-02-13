#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Socket very useful to connect to every sh*t in da world"""
import socket

"""I want da model"""
from Model.Device import device
from Model.Device import sensor 
from Model.Device import switch
from Model.Device import temperature
from Model.Device import actuator
from Model.Device import historic
from traductor.trame import trame

"""I want da logger"""
import logger.loggerConfig as myLog

from user import *
from mongoengine import *


logger=myLog.configure()
connect('test')
   


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
        Sum up all the bytes of the trame except sep and return the 2 last byte
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

    def translateTemp(self,trameUsed):
        """
        return the temperature (range 0-40 c) from data byte 2 
        """
        rowTemp=int(trameUsed.data1,16)
        temp = rowTemp*40/255.0
        return temp


    def checkTrame(self):
        logger.info("Trame used : {}".format(self.trameUsed.rawView()))
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
                if (self.trameUsed.data0=='09'):
                    logger.info("Door sensor {} with state [close]".format(self.trameUsed.ident))
                    newData = True
                elif (self.trameUsed.data0=='08'):
                    logger.info("Door sensor {} with state [open]".format(self.trameUsed.ident))
                    newData = False
                else:
                    logger.info("Strange state : ".format(self.trameUsed.data2))
            elif (sensorUsed.__class__.__name__=="Temperature"):
                newData = self.translateTemp(self.trameUsed)
                logger.info("Temperature sensor {} with temp {}".format(self.trameUsed.ident, newData))
            else :
                logger.info("Other Captor (not handle (YET !) )")
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
