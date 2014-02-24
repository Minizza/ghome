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
        if (str(daNewState)=="toggle"):
            if self.current_state=="off":
                #on met à on
                rawTrame="A55A6B0570000000"+ "FF9F1E0"+"7" +"30"
                self.current_state="on"
            elif(self.current_state=="on"):
                #on met à off
                rawTrame="A55A6B0550000000"+ "FF9F1E0"+"7" +"30"
                self.current_state="off"
        else:
            LOGGER.warn("Strange new state : {}. Trram not send".format(daNewState))
            return ""
        LOGGER.info("State after : {}".format(self.current_state))
        myTrame=Trame.trame(rawTrame)
        myTrame.calculateChecksum()
        LOGGER.info("Actuator trame generated, to be send : {}".format(myTrame.lessRawView()))
        self.save()
        return myTrame.rawView()