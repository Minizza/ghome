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

path = "../traducteur"
sys.path.append(path)

from traductor import *
from fakeJerome import *

from mongoengine import *



connect('test')


########################################################################
# Tests for FakeJerome trameGetting
########################################################################
def fakeJerome_test():
	#Deleting pre-existing peripherique to clean the test database
	for device in Device.objects:
		device.delete()
		
	capteur1 = Sensor(physic_id = "12230EAF", name = "CAPTEUR1_CUISINE", current_state = 19)
	
	capteur1.save()
	
	for device in Device.objects:
		print device.physic_id, " ", device.current_state
	
########################################################################

if __name__== '__main__':
	fakeJerome_test()
