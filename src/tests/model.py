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
# Tests for Utilisateur base
########################################################################
def user_test():
	#Deleting pre-existing users to clean the test database
	for user in User.objects:
		user.delete()

	user1 = User(name = "Dupont", password = "test", role = "Basic")
	user2 = User(name = "Martin", password = "pass", role = "Admin")

	#Adding new users
	user1.save()
	user2.save() 

	#Invalid user: name is missing (uncomment to test)
	#user3 = User(password = "f*ck", role = "Basic")	
	#user3.save()
		
	#Printing users in Utilisateur base
	for user in User.objects:
		print user.id, " ", user.name, " ", user.password, " ", user.role
########################################################################


########################################################################
# Tests for Peripherique base
########################################################################
def peripherique_test():
	#Deleting pre-existing peripherique to clean the test database
	for device in Device.objects:
		device.delete()
		
	capteur1 = Sensor(physic_id = "12230EAF", current_state = BooleanField())
	capteur1.current_state = False
	capteur1.save()
	
	for device in Device.objects:
		print device.physic_id, " ", current_state
	
########################################################################
