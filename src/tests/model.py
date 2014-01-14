# -*-coding:Utf-8 -*

import sys
path = "../Model/Device/"
sys.path.append(path)

from peripherique import *
from capteur import *
from actionneur import *
from historique import *

path = "../Model/User/"
sys.path.append(path)

from utilisateur import *

from mongoengine import *

connect('test')


########################################################################
# Tests for Utilisateur base
########################################################################
def user_test():
	#Deleting pre-existing users to clean the test database
	for user in Utilisateur.objects:
		user.delete()

	user1 = Utilisateur(nom = "Dupont", mdp = "test", role = "Basic")
	user2 = Utilisateur(nom = "Martin", mdp = "pass", role = "Admin")

	#Adding new users
	user1.save()
	user2.save() 

	#Invalid user: name is missing (uncomment to test)
	#user3 = Utilisateur(mdp = "f*ck", role = "Basic")	
	#user3.save()
		
	#Printing users in Utilisateur base
	for user in Utilisateur.objects:
		print user.id, " ", user.nom, " ", user.mdp, " ", user.role
########################################################################


########################################################################
# Tests for Peripherique base
########################################################################
#def peripherique_test():
	#Deleting pre-existing peripherique to clean the test database
	
