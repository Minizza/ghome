#!/usr/bin/env 
# -*- coding: utf-8 -*-
from mongoengine import *
from logger import LOGGER

class lazzyUpdate(Document):
    """
        Tuple frequently checked by the traductor to update a sensor
    """

    id = ObjectIdField(required = True)
    idToUpdate = StringField()#if not set to something upate all captor
    newState = DynamicField()

    def updateAll(self):
    	"""
    		Ask for update of all sensors
    	"""
    	self.idToUpdate=''
    	self.newState=''
    	self.save()

    def updateOne(self,ident):
    	"""
    		Ask for update the sensor with this id
    	"""
    	LOGGER.debug("lazily updating {}".format(ident))
    	self.idToUpdate=ident
    	self.newState=''
    	self.save()

    def sendTrame(self,ident,newstate):
    	"""
    		Ask the traductor to send a trame with the new state of a captor
    	"""
    	self.idToUpdate=ident
    	self.newState=newstate
    	self.save()
