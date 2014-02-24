# -*-coding:Utf-8 -*
from device import *
from logger import LOGGER
from traducteur import Trame
 
class Actuator(Device):
    """Classe pour les actionneurs"""

    """
        current state 
            on
            off

    """
    def gimmeTrame(self,daNewState):
        """
            Return the update trame to be sent
        """
        if (daNewState=="on"):
            rawTrame="A55A6B0570000000"+ self.physic_id +"30"
        elif(daNewState=="off"):
            rawTrame="A55A6B0550000000"+ self.physic_id +"30"
        else:
            LOGGER.warn("Strange new state : {}. Trram not send".format(daNewState))
            return ""
        myTrame=Trame.trame(rawTrame)
        myTrame.calculateChecksum()
        LOGGER.info("Trame generated, to be send : {}".format(myTrame.lessRawView()))
        return myTrame.rawView()