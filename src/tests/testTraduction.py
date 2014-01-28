# -*-coding:Utf-8 -*

import socket
import thread

import unittest2

import sys
path = "../Model/Device/"
sys.path.append(path)

from device import *
from sensor import *
from switch import *
from actuator import *
from historic import *

path = "../Model/User/"
sys.path.append(path)

from user import *

path = "../traducteur"
sys.path.append(path)

from traductor import *
from fakeJerome import *

from mongoengine import *



connect('test')


def send_trame():
		chan = server.bind(('', 1515))    
		server.listen(5)  
		c,adrr = server.accept()
		c.send('A55A0B06000000090001B25E002B')

thread.start_new_thread(send_trame,())

class ModelTest(unittest2.TestCase):
	########################################################################
	# Tests for FakeJerome trameGetting
	########################################################################
	def test_fakeJerome(self):
		#Deleting pre-existing peripherique to clean the test database
		for device in Device.objects:
			device.delete()
			
		capteur1 = Sensor(physic_id = "12230EAF", name = "CAPTEUR1_CUISINE", current_state = 19)
		
		capteur1.save()

		tram = trame('A55A0B06000000080001B25E002A')
		capteur = Switch(physic_id = tram.ident, name = "INTERRUPTEUR_PLAQUE", current_state = False)
		capteur.save()

		for device in Device.objects:
			print device.physic_id, " ", device.current_state

		tradMeThis = traductor()
		tradMeThis.connect('',1515)
		tradMeThis.receive()
		tradMeThis.checkTrame()

		comparedCapt = Sensor.objects(physic_id=tram.ident)[0]
		print comparedCapt.current_state
		self.assertTrue(comparedCapt.current_state)

		for device in Device.objects:
			print device.physic_id, " ", device.current_state
		
########################################################################

if __name__== '__main__':
	unittest2.main()
