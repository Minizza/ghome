#!/usr/bin/python
# -*- coding: utf-8 -*-

"""I want da logger"""
import logger.loggerConfig as myLog

logger=myLog.configure()

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
        self.data3 = receivedData[8:10]
        self.data2 = receivedData[10:12]
        self.data1 = receivedData[12:14]
        self.data0 = receivedData[14:16]
        self.ident = receivedData[16:24]
        self.flag = receivedData[24:26]
        if(len(receivedData)>26):
        	self.checkSum = receivedData[26:]
    
    def nameIt (self) :
        logger.info("{} is a {} ".format(self.ident,self.rOrg))

    def lessRawView(self):
        return self.sep + self.length+self.rOrg+" "+self.data3+self.data2+self.data1+self.data0+" "+self.ident+" "+self.flag+self.checkSum

    def rawView(self):
        return self.sep + self.length+self.rOrg+self.data3+self.data2+self.data1+self.data0+self.ident+self.flag+self.checkSum

    def calculateChecksum(self):
        """
        Sum up all the bytes of the trame except sep and take the 2 last byte
        Then update the checksum value
        """
        sum=0
        sum+=int(self.length,16)
        sum+=int(self.rOrg,16)
        sum+=int(self.data0,16)
        sum+=int(self.data1,16)
        sum+=int(self.data2,16)
        sum+=int(self.data3,16)
        sum+=int(self.ident[:2],16)
        sum+=int(self.ident[2:4],16)
        sum+=int(self.ident[4:6],16)
        sum+=int(self.ident[6:8],16)
        sum+=int(self.flag,16)
        sum=hex(sum)
        self.checkSum = sum[(len(sum)-2):].upper()