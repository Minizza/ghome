# -*-coding:Utf-8 -*
from sensor import *
from logger import LOGGER


class Switch(Sensor):
	"""Switch class"""

	def translateTrame(self,inTrame):
		"""
		return 	close if data0=09, 
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