#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Socket very useful to connect to every sh*t in da world"""
import socket
import threading
import sys

"""I want da model"""
from Model.Device import device
from Model.Device import sensor 
from Model.Device import switch
from Model.Device import temperature
from Model.Device import actuator
from Model.Device import historic
from traducteur import trame 

"""I want da logger"""
from logger import LOGGER

from user import *
from mongoengine import *


connect('test')
   
    

class traductor ():
    """
    TODO écrire la doc

    """

    def __init__ (self) :
        """
            Create things for synchro, get the sensors from the DB
        """
        self.lock=threading.Lock()#Lock use for DB updates
        self.soc = socket.socket()
        self.stoppedAnalyze=False
        self.trameUsed = ''
        self.identSet = set()
        #Load all the device in the base
        self.updateIdentSet()
        with self.lock:
            for lsensor in sensor.Sensor.objects:
                self.identSet.append(lsensor.physic_id)
                LOGGER.info(lsensor.physic_id)

    def connect (self, addr, port) :
        self.soc.connect((addr,port))
        LOGGER.info("Connected to {} : {}".format(addr,port))
    
    def receive (self) :
        message = self.soc.recv(1024)
        LOGGER.debug("trame reçu")
        if message and len(message)==28:
            self.trameUsed = trame.trame(message)

    def launch(self,addr,port):
        try:
            self.connect(addr,port)
        except socket.error,e:
            raise e
        dacount=0
        while 1:
            try:
                if dacount >10000 : self.updateIdentSet()
                self.receive()
                if self.trameUsed:
                    self.checkTrame()
                dacount+=1
            except KeyboardInterrupt:
                sys.exit(0)


            

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


    def checkTrame(self):
        LOGGER.info("Trame used : {}".format(self.trameUsed.lessRawView()))
        if ("A55A" not in self.trameUsed.sep):
            LOGGER.warn("Wrong separator, rejected")

        if (self.doChecksum(self.trameUsed) not in self.trameUsed.checkSum):     
            #Mauvais checkSum
            LOGGER.warn("Wrong checksum, expected : {}, rejected".format(self.doChecksum(self.trameUsed)))

        with self.lock:
            if (self.trameUsed.ident in self.identSet):
                #Recuperer le capteur en bdd
                sensorUsed = sensor.Sensor.objects(physic_id=self.trameUsed.ident)[0]
                #Identifier le type de trame && Traiter les data de la trame
                newData = '' #la nouvelle data a entrer en base, type dynamique
                if (sensorUsed.__class__.__name__=="Switch"):
                    newData=sensorUsed.translateTrame(self.trameUsed)
                elif (sensorUsed.__class__.__name__=="Temperature"):
                    newData = sensorUsed.translateTrame(self.trameUsed)

                elif (sensorUsed.__class__.__name__=="Position"):
                    newData = sensorUsed.translateTrame(self.trameUsed)
                else :
                    LOGGER.warn("Other Captor (not handle (YET !) )")
                # Update de la trame au niveau de la base
                if newData :
                    sensorUsed.update(newData)
                    LOGGER.info("New data {}".format(sensorUsed.current_state))
        self.trameUsed=''
            

    def updateIdentSet(self):
        """
            Safely update the identifier set of the traductor
        """
        with self.lock:
            #del(self.identSet[:])
            self.identSet=[]
            for lsensor in sensor.Sensor.objects:
                self.identSet.append(lsensor.physic_id)
                LOGGER.info(lsensor.physic_id)
            LOGGER.info("Traductor's set of captors updated")



if __name__ == '__main__':
    connect('test')
    # soc = socket.socket()
    # soc.connect(('',1515))
    # LOGGER.info("Connection")
    # try:
    #     while 1 :
    #         message = soc.recv(1024)
    #         if message:
    #             tram2 = trame.trame(message)
    #             print tram2.lessRawView()
    # except socket.error:
    #     LOGGER.info("Déconnection du serveur")
    #     soc.close()
    try:
        myTrad=traductor()
        myTrad.launch('',1515)
    except socket.error:
        LOGGER.info("Déconnection du serveur")
    finally:
        pass
