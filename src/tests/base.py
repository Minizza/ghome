# -*-coding:Utf-8 -*

from mongoengine import *

import sys
import datetime
import Model.Device.device as ghomedevice
import Model.Device.sensor as sensor
import Model.Device.actuator as actuator
import Model.Device.temperature as temperature
import Model.Device.switch as switch
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

	#list of actuators
	device2 = actuator.Actuator(physic_id = "AB2424DC", name = "Actionneur zombie apocalypse", coordX = 65, coordY = 530)

	#list of temperature sensors
	device3 = temperature.Temperature(physic_id = "AZ3RT1UI0P", name = "Capteur température cuisine", current_state = "15", coordX = 500, coordY = 200)
	device4 = temperature.Temperature(physic_id = "A23RG45I07", name = "Capteur température bureau", current_state = "20", coordX = 200, coordY = 500)

	#list of switch sensors
	device5 = switch.Switch(physic_id = "AJI24MF5", name = "Plaque pression couloir", current_state = "False", coordX = 300, coordY = 400)
	device6 = switch.Switch(physic_id = "ADKE334D", name = "Plaque pression hangar", current_state = "False", coordX = 400, coordY = 300)
	device7 = switch.Switch(physic_id = "A457GT6D", name = "Détecteur présence bureau", current_state = "False", coordX = 100, coordY = 400)
	device8 = switch.Switch(physic_id = "ABGB45PL", name = "Détecteur présence salon", current_state = "False", coordX = 400, coordY = 100)
	device9 = switch.Switch(physic_id = "RT524EDR", name = "Porte chambre", current_state = "False", coordX = 250, coordY = 80)

	#Adding new users
	device1.save()
	device2.save()
	device3.save()
	device4.save()
	device5.save()
	device6.save()
	device7.save()
	device8.save()
	device9.save()

	#Printing users in Utilisateur base
	for device in ghomedevice.Device.objects:
		print device.id, " ", device.physic_id, " ", device.name
########################################################################
device_test()
