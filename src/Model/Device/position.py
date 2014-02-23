# -*-coding:Utf-8 -*
from sensor import *
from mongoengine import *
from logger import LOGGER
from Model.update import lazzyUpdate
from traducteur import trame


 
class Position(Sensor):

    """Class for position sensor"""
    maxX=610
    maxY=545
    trameStart="A55A4242"
    trameEnd ="FF"

    """New field in order to know the team of the sensor"""
    team = IntField()


    def translateTrame(self,inTrame):
        """
            convert 4 bytes to a value in range (0 - maxX) (resp Y)
        """
        rawConvertedY=int((inTrame.data1+inTrame.data0),16)
        rawConvertedX=int((inTrame.data3+inTrame.data2),16)
        absX=int(round(rawConvertedX/(16**4-1.0)*self.maxX))
        absY=int(round(rawConvertedY/(16**4-1.0)*self.maxY))
        LOGGER.info("Position sensor {} with new coordonate {} -- {}".format(self.physic_id,absX,absY))
        return {"coordX":absX,"coordY":absY}

    def gimmeTrame(self,daNewState):
        """
            Return the update trame to be sent
        """
        newCoord=self.translateCoord(daNewState.get('coordX'),daNewState.get('coordY'))
        strTrame=self.trameStart+newCoord.get('x')+newCoord.get('y')+self.physic_id+self.trameEnd
        myTrame=trame.trame(strTrame)
        myTrame.calculateChecksum()
        LOGGER.debug("Trame returned : {}".format(myTrame.rawView()))
        return myTrame

    def moving(self,newX,newY):
        """
            Simulate the movement of the captor
        """
        LOGGER.debug("{} moved to {} | {}".format(self.physic_id,newX,newY))
        lazzyUpdate().sendTrame(self.physic_id,{"coordX":newX,"coordY":newY})

    def translateCoord(self,absX,absY):
        """
            convert absolute coordonate to 4 Bytes value
        """
        rawConvertedX=hex(absX*(16**4-1)/self.maxX).upper()
        rawConvertedY=hex(absY*(16**4-1)/self.maxY).upper()
        return {'x':rawConvertedX[2:],'y':rawConvertedY[2:]}      