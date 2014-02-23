# -*-coding:Utf-8 -*
from sensor import *
from logger import LOGGER
from traducteur import trame

class Switch(Sensor):
    """Switch class"""

    trameStart="A55A0B06"
    trameEnd="00"

    def translateTrame(self,inTrame):
        """
        return  close if data0=09, 
                open if data0=08 
                else nothing
        """
        if (inTrame.data0=='09'):
                        LOGGER.info("Door sensor {} with state [close]".format(inTrame.ident))
                        dataToRet = "close"
        elif(inTrame.data0=='08'):
            LOGGER.info("Door sensor {} with state [open]".format(inTrame.ident))
            dataToRet = "open"
        else:
            LOGGER.warn("Door sensor {}Strange state : {}".format(inTrame.ident, inTrame.data2))
            dataToRet=''
        return dataToRet

    def gimmeTrame(self,daNewState):
        """
            Return the update trame to be sent
        """
        if daNewState=="close":
            data="00000009"
        elif daNewState=="open":
            data="00000008"
        else :
            LOGGER.warn("Strange state : {}. Trame not sent".format(daNewState))
            return ""
        strTrame=elf.trameStart+data+self.physic_id+self.trameEnd
        myTrame=trame.trame(strTrame)
        myTrame.calculateChecksum()
        LOGGER.debug("Trame returned : {}".format(myTrame.rawView()))
        return myTrame.rawView()