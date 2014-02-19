# -*-coding:Utf-8 -*
from sensor import *
from mongoengine import *
 
class Position(Sensor):

	"""Class for position sensor"""
	maxX=IntField()
	maxY=IntField()