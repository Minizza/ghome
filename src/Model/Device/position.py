# -*-coding:Utf-8 -*
from sensor import *
from mongoengine import *
 
class Position(Sensor):

	"""Class for position sensor"""
	maxX=610
	maxY=545
	trameStart="A55A4242"
	trameEnd ="FF"