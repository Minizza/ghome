# -*-coding:Utf-8 -*
from sensor import *
from logger import LOGGER


class Temperature(Sensor):
    
    minTemp = IntField()
    maxTemp = IntField()

    def translateTrame(self,inTrame):
        """
        return the temperature (range 0-40 c) from data byte 2 
        """
        rowTemp=int(inTrame.data1,16)
        temperature = round((rowTemp*40/255.0),3)
        LOGGER.info("Temperature sensor {} with temp {}".format(inTrame.ident, temperature))
        return temperature
