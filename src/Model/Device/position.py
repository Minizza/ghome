# -*-coding:Utf-8 -*
from sensor import *
from mongoengine import *
 
class Position(Sensor):

	"""Class for position sensor"""
	maxX=610
	maxY=545
	trameStart="A55A4242"
	trameEnd ="FF"

	def translateTrame(self,inTrame):
		"""

		"""
		print inTrame.lessRawView()
		rawConvertedX= int((inTrame.data1+inTrame.data0),16)
		rawConvertedY=int((inTrame.data3+inTrame.data2),16)
		absX=rawConvertedX/(16**4-1.0)*self.maxX