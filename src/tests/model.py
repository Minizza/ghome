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
	for user in Utilisateur.objects:
		user.delete()

	user1 = Utilisateur(name = "Dupont", password = "test", role = "Basic")
	user2 = Utilisateur(name = "Martin", password = "pass", role = "Admin")

	#Adding new users
	user1.save()
	user2.save() 

	#Invalid user: name is missing (uncomment to test)
	#user3 = Utilisateur(password = "f*ck", role = "Basic")	
	#user3.save()
		
	#Printing users in Utilisateur base
	for user in Utilisateur.objects:
		print user.id, " ", user.name, " ", user.password, " ", user.role
########################################################################


########################################################################
# Tests for Peripherique base
########################################################################
def peripherique_test():
	#Deleting pre-existing peripherique to clean the test database
	for device in Peripherique.objects:
		device.delete()
		
	capteur1 = Capteur(id_physique = "12230EAF", current_state = False)
	
	capteur1.save()
	
	for device in Peripherique.objects:
		print device.id_physique, " ", current_state
	
########################################################################
