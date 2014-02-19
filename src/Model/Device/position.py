# -*-coding:Utf-8 -*
from sensor import *
from mongoengine import *
from logger import loggerConfig

logger=loggerConfig.configure()

 
class Position(Sensor):

	"""Class for position sensor"""
	maxX=610
	maxY=545
	trameStart="A55A4242"
	trameEnd ="FF"

	def translateTrame(self,inTrame):
		"""
			convert 4 bytes to a value in range (0 - maxX) (resp Y)
		"""
		
		rawConvertedX= int((inTrame.data1+inTrame.data0),16)
		rawConvertedY=int((inTrame.data3+inTrame.data2),16)
		absX=rawConvertedX/(16**4-1.0)*self.maxX
		absY=rawConvertedY/(16**4-1.0)*self.maxY
		logger.info("Position sensor {} with new coordonate {} -- {}".format(self.physic_id,absX,absY))
		return {"coordX":absX,"coordY":absY}