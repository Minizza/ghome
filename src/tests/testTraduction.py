# -*-coding:Utf-8 -*

import sys
path = "../Model/Device/"
sys.path.append(path)

from device import *
from sensor import *
from actuator import *
from historic import *

path = "../Model/User/"
sys.path.append(path)

from user import *

from mongoengine import *

connect('test')


########################################################################
# Tests for FakeJerome trameGetting
########################################################################
def fakeJerome_test():
	#Deleting pre-existing peripherique to clean the test database
	for device in Device.objects:
		device.delete()
		
	capteur1 = Sensor(id_physique = "12230EAF", current_state = "False")
	
	capteur1.save()
	
	for device in Device.objects:
		print device.id_physique, " ", current_state
	
########################################################################
