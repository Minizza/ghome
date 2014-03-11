#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Socket very useful to connect to every sh*t in da world"""
import socket
import threading
import sys

"""I want da model"""
from Model.Device import device
from Model.Device import sensor 
from Model.update import lazzyUpdate
from Model.Device import position
from traducteur import Trame 

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
        self.running=True
        self.identSet = set([])
        lazzyUpdate.drop_collection()
        LOGGER.info("initializing sensors set : ")
        for lsensor in sensor.Sensor.objects:
                    self.identSet.add(lsensor.physic_id)
                    LOGGER.info(lsensor.physic_id)

    def connect (self, addr, port) :
        self.soc.connect((addr,port))
        self.soc.setblocking(0)
        LOGGER.info("Connected to {} : {}".format(addr,port))
    
    def receive (self) :
        # LOGGER.debug("en attente de trame")
        message = self.soc.recv(1024)
        if message and len(message)==28:
            LOGGER.debug("trame reçu : {}".format(message))
            self.trameUsed = Trame.trame(message)
        else :
            return

    def launch(self,addr,port):
        self.connect(addr,port)
        dacount=0
        self.updateIdentSet()
        while self.running:
            try:
                if dacount >200 : #Fréquence de mise à jour de la base
                    self.updateIdentSet()
                    dacount=0
                try:
                    self.receive()
                except IOError:
                    # timeout !
                    pass
                if self.trameUsed:
                    self.checkTrame()
                dacount+=1
                # LOGGER.debug("tic")
            except KeyboardInterrupt:
                sys.exit(0)
        LOGGER.info("Le traducteur est terminé")

    def stop(self):
        self.running=False

    

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
        if self.trameUsed:
            LOGGER.debug("Trame received : {}".format(self.trameUsed.lessRawView()))
            if ("A55A" not in self.trameUsed.sep):
                LOGGER.warn("Wrong separator, rejected")

            if (self.doChecksum(self.trameUsed) not in self.trameUsed.checkSum):     
                #Mauvais checkSum
                LOGGER.warn("Wrong checksum, expected : {}, rejected".format(self.doChecksum(self.trameUsed)))

            with self.lock:
                if (self.trameUsed.ident in self.identSet):
                    #Recuperer le capteur en bdd
                    sensorUsed = sensor.Sensor.objects(physic_id=self.trameUsed.ident)[0]
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
                        LOGGER.info(" Sensor {} ||New data {}".format(sensorUsed.physic_id, sensorUsed.current_state))
            self.trameUsed=''
            
        
    def sendTrame(self,ident,newState):
        with self.lock:
            sensorUsed=sensor.Device.objects(physic_id=ident)[0]
        daTrame=sensorUsed.gimmeTrame(newState)
        if daTrame:
            self.soc.send(daTrame)
            LOGGER.info("Trame sended : {}".format(daTrame))
            return
                

    def updateIdentSet(self):
        """
            Safely update the identifier set of the traductor
        """
        for anUpdate in lazzyUpdate.objects:
            LOGGER.warn("id : {} || state : {}".format(anUpdate.idToUpdate,anUpdate.newState))
            if(anUpdate.idToUpdate==""):
                with self.lock:
                    self.identSet=set([])
                    for lsensor in sensor.Sensor.objects:
                        self.identSet.add(lsensor.physic_id)
                        LOGGER.info(lsensor.physic_id)
                    LOGGER.info("Traductor's set of captors updated")
            elif(anUpdate.newState==""):
                with self.lock:
                    if (anUpdate.idToUpdate in things.physic_id for things in sensor.Sensor.objects):
                        self.identSet.add(anUpdate.idToUpdate)
                        LOGGER.info("{} added".format(anUpdate.idToUpdate))
            else:
                #send a trame from a captor with a newState
                LOGGER.error("Sensor to update : {} ||new state : {}".format(anUpdate.idToUpdate,anUpdate.newState))
                self.sendTrame(anUpdate.idToUpdate,anUpdate.newState)
            anUpdate.delete()
            LOGGER.warn(" {} update           GROS delete de : {} || {}".format(lazzyUpdate.objects.count(),anUpdate.idToUpdate,anUpdate.newState))
            return 
        LOGGER.debug("nothing to update")




if __name__ == '__main__':
    connect('test')
    try:
        myTrad=traductor()
        myTrad.launch('',1515)
    except socket.error:
        LOGGER.info("Déconnection du serveur")
        mytrad.soc.close()
    finally:
        pass
