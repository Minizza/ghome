# -*-coding:Utf-8 -*

from mongoengine import *

import sys
import datetime
import Model.Device.device as ghomedevice
import Model.Device.sensor as sensor
import Model.Device.actuator as actuator
import Model.Device.temperature as temperature
import Model.Device.historic as historic
import Model.Draw.draw as draw 
import Model.Draw.form as form
import Model.Place.place as place
import Model.Place.ghomeuser as ghomeuser

connect('test')


########################################################################
# Tests for User base
########################################################################
def user_test():
	#Deleting pre-existing users to clean the test database
	ghomeuser.GHomeUser.drop_collection()

	user1 = ghomeuser.GHomeUser(name = "Dupont", password = "test", role = "")
	user2 = ghomeuser.GHomeUser(name = "Martin", password = "pass", role = "admin")

	#Adding new users
	user1.save()
	user2.save() 

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
	device2 = actuator.Actuator(physic_id = "AB2424DC", name = "Actionneur zombie apocalypse", coordX = 25, coordY = 550)
	device3 = temperature.Temperature(physic_id = "AZ3RT1UI0P", name = "Capteur température n°1", current_state = "15")


	#Adding new users
	device1.save()
	device2.save()
	device3.save()

	#Printing users in Utilisateur base
	for device in ghomedevice.Device.objects:
		print device.id, " ", device.physic_id, " ", device.name
########################################################################
device_test()
