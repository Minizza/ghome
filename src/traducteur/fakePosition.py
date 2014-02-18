# -*-coding:Utf-8 -*

from mongoengine import *

class fakePosition():

	position = [0, 0, 0]

	def setPosition(self, x, y, z):
		self.position = [x, y , z]


	def sendTrame():
		trame = ""
		return trame