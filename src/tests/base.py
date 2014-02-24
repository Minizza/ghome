# -*-coding:Utf-8 -*

from mongoengine import *

import sys
import datetime
import math
import thread
import Model.Device.device as ghomedevice
import Model.Device.sensor as sensor
import Model.Device.actuator as actuator
import Model.Device.temperature as temperature
import Model.Device.switch as switch
import Model.Device.position as position
import Model.Device.historic as historic
import Model.Draw.draw as draw 
#import Model.Draw.form as form
import Model.Place.place as place
import Model.Place.ghomeuser as ghomeuser

connect('test')


########################################################################
# Tests for User base
########################################################################
def user_test():
	#Deleting pre-existing users to clean the test database
	ghomeuser.GHomeUser.drop_collection()

	user1 = ghomeuser.GHomeUser(name = "Gerant", password = "admin", role = "admin")
	user2 = ghomeuser.GHomeUser(name = "Joueur1", password = "pass1", role = "player")
	user3 = ghomeuser.GHomeUser(name = "Joueur2", password = "pass2", role = "player")
	user4 = ghomeuser.GHomeUser(name = "Chef1", password = "passChef1", role = "chief")
	user5 = ghomeuser.GHomeUser(name = "Chef2", password = "passChef2", role = "chief")

	#Adding new users
	user1.save()
	user2.save() 
	user3.save()
	user4.save()
	user5.save()

	#Invalid user: name is missing (uncomment to test)
	#user3 = ghomeuser.GHomeUser(password = "f*ck", role = "Basic")	
	#user3.save()
		
	#Printing users in Utilisateur base
	for user in ghomeuser.GHomeUser.objects:
		print user.id, " ", user.name, " ", user.password, " ", user.role
########################################################################
user_test()


########################################################################
# Tests for Device base
########################################################################
def device_test():
	#Deleting pre-existing users to clean the test database
	ghomedevice.Device.drop_collection()

	device1 = sensor.Sensor(physic_id = "AB4242CD", name = "Détecteur de fin du monde", coordX = 300, coordY = 400)

	#list of actuators
	device2 = actuator.Actuator(physic_id = "AB2424DC", name = "Actionneur zombie apocalypse", coordX = 65, coordY = 330)

	#list of temperature sensors
	device3 = temperature.Temperature(physic_id = "AZ3DF1UI09", name = "Capteur température cuisine", current_state = "15", coordX = 500, coordY = 200)
	device4 = temperature.Temperature(physic_id = "A23FB45I07", name = "Capteur température bureau", current_state = "20", coordX = 200, coordY = 500)

	#list of switch sensors
	device5 = switch.Switch(physic_id = "ACF24EF5", name = "Plaque pression couloir", current_state = "False", coordX = 300, coordY = 400)
	device6 = switch.Switch(physic_id = "AD8E334D", name = "Plaque pression hangar", current_state = "True", coordX = 400, coordY = 300)
	device7 = switch.Switch(physic_id = "A457FE6D", name = "Détecteur présence bureau", current_state = "False", coordX = 100, coordY = 400)
	device8 = switch.Switch(physic_id = "ABFB454E", name = "Détecteur présence salon", current_state = "False", coordX = 400, coordY = 100)
	device9 = switch.Switch(physic_id = "DF524ED5", name = "Porte chambre", current_state = "False", coordX = 250, coordY = 80)

	#list of players
		# A player is just represented by a coordonate getting sensor
	player11 = position.Position(physic_id = "AFEFE327", name = "Equipe 1 joueur 1", current_state = 1, coordX = 50, coordY = 500)
	player12 = position.Position(physic_id = "BF4586CD", name = "Equipe 1 joueur 2", current_state = 1, coordX = 60, coordY = 500)
	player13 = position.Position(physic_id = "DE42651C", name = "Equipe 1 joueur 3", current_state = 1, coordX = 70, coordY = 500)
	player14 = position.Position(physic_id = "A13542F5", name = "Equipe 1 joueur 4", current_state = 1, coordX = 60, coordY = 510)
	player15 = position.Position(physic_id = "FD5E42CD", name = "Equipe 1 joueur 5", current_state = 1, coordX = 50, coordY = 510)
	player21 = position.Position(physic_id = "AB4FDF5D", name = "Equipe 2 joueur 1", current_state = 2, coordX = 600, coordY = 50)
	player22 = position.Position(physic_id = "DE25F5CD", name = "Equipe 2 joueur 2", current_state = 2, coordX = 600, coordY = 60)
	player23 = position.Position(physic_id = "EBB65542", name = "Equipe 2 joueur 3", current_state = 2, coordX = 600, coordY = 70)
	player24 = position.Position(physic_id = "FDE4E358", name = "Equipe 2 joueur 4", current_state = 2, coordX = 590, coordY = 60)
	player25 = position.Position(physic_id = "3255G467", name = "Equipe 2 joueur 5", current_state = 2, coordX = 590, coordY = 50)


	#Adding new sensors or actuators
	device1.save()
	device2.save()
	device3.save()
	device4.save()
	device5.save()
	device6.save()
	device7.save()
	device8.save()
	device9.save()

	#Adding new players
	player11.save()
	player12.save()
	player13.save()
	player14.save()
	player15.save()
	player21.save()
	player22.save()
	player23.save()
	player24.save()
	player25.save()


	#Printing users in Utilisateur base
	for device in ghomedevice.Device.objects:
		print device.id, " ", device.physic_id, " ", device.name

	def loop() : 
		ang = 0
		while True:
			player11.coordX = 500*(1-math.cos(ang)*math.cos(ang))
			player11.coordY = 500*(1-math.cos(ang)*math.cos(ang))
			ang += 0.001
			player11.save()

	thread.start_new_thread(loop,())
########################################################################
device_test()
