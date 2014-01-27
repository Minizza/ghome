# -*-coding:Utf-8 -*

from mongoengine import *

import sys
import datetime
import Model.Device.device as ghomedevice
import Model.Device.sensor as sensor
import Model.Device.actuator as actuator
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

	#user1
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
	#Deleting pre-existing devices to clean the test database
	ghomedevice.Device.drop_collection()
	
	#Setting a date field and a state field
	dateField = [datetime.datetime.now(), datetime.datetime.now()]
	stateField = [25, 22]
	
	#capteur1: no historic at creation, uses add_state() and setCurrentState()	
	capteur1 = sensor.Sensor(physic_id = "12230EAF", name = "CAPTEUR1_CUISINE", current_state = 19)
	capteur1.save()
	capteur1.addState(datetime.datetime.now(), capteur1.current_state)
	capteur1.setCurrentState(20)
	
	#actuator1: no historic at creation, uses setHistoric()
	actuator1 = actuator.Actuator(physic_id = "4562312AAA", name = "ACTIONNEUR2_TOILETTE", current_state = "OPEN")
	actuator1.save()
	historic1 = historic.Historic(date = dateField, state = stateField)
	actuator1.setHistoric(historic1)
	
	#Invalid device: duplicate ID (uncomment to test)
	#actuator2 = actuator.Actuator(physic_id = "12230EAF", name = "ACTIONNEUR_WRONG", current_state = "CLOSED")
	#actuator2.save()
	
	historic2 = historic.Historic(date = dateField, state = stateField)
	historic2.save()
	
	#capteur2: historic at creation, use addState()
	capteur2 = sensor.Sensor(physic_id = "AEFF4242", name = "CAPTEUR2_CUISINE", current_state = 22, historic = historic2)
	capteur2.save()
	capteur2.addState(datetime.datetime.now(), 27)

	#Print all devices' info'
	for device in ghomedevice.Device.objects:
		print device.physic_id, " ", device.name, " ", device.current_state
		if device.historic:
			print device.historic.date, " ", device.historic.state	
########################################################################


########################################################################
# Tests for Draw base
########################################################################
def draw_test():
	#Deleting pre-existing draws to clean the test database
	draw.Draw.drop_collection()	
