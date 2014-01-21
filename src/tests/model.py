# -*-coding:Utf-8 -*

from mongoengine import *

import sys
import datetime

path = "../Model/Device/"
if path not in sys.path:
	sys.path.append(path)

import device as ghomedevice
import sensor
import actuator
import historic

path = "../Model/Draw/"
if path not in sys.path:
	sys.path.append(path)

import draw
import form
	
path = "../Model/Place"
if path not in sys.path:
	sys.path.append(path)

import place
import ghomeuser

connect('test')


########################################################################
# Tests for User base
########################################################################
def user_test():
	#Deleting pre-existing users to clean the test database
	ghomeuser.GHomeUser.drop_collection()

	user1 = ghomeuser.GHomeUser(name = "Dupont", password = "test", role = "Basic")
	user2 = ghomeuser.GHomeUser(name = "Martin", password = "pass", role = "Admin")

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


########################################################################
# Tests for Device base
########################################################################
def device_test():
	#Deleting pre-existing peripherique to clean the test database
	ghomedevice.Device.drop_collection()
		
	capteur1 = sensor.Sensor(physic_id = "12230EAF", name = "CAPTEUR1_CUISINE", current_state = 19)
	capteur1.save()
	
	actuator1 = actuator.Actuator(physic_id = "4562312AAA", name = "ACTIONNEUR2_TOILETTE", current_state = "OPEN")
	actuator1.save()
	
	#Invalid device: duplicate ID (uncomment to test)
	#actuator2 = actuator.Actuator(physic_id = "12230EAF", name = "ACTIONNEUR_WRONG", current_state = "CLOSED")
	#actuator2.save()
	
	dateField = [datetime.datetime.now(), datetime.datetime.now()]
	stateField = [25, 22]
	historic1 = historic.Historic(date = dateField, state = stateField)
	
	historic1.save()
	
	capteur2 = sensor.Sensor(physic_id = "AEFF4242", name = "CAPTEUR2_CUISINE", current_state = 22, historic = historic1)
	capteur2.save()
	
	for device in ghomedevice.Device.objects:
		print device.physic_id, " ", device.name, " ", device.current_state
		if device.historic:
			print device.historic.date, " ", device.historic.state
	
########################################################################
