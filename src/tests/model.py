# -*-coding:Utf-8 -*

from mongoengine import *

import sys
import datetime

import unittest2

import Model.Device.device as ghomedevice

import Model.Device.sensor as sensor
import Model.Device.actuator as actuator
import Model.Device.temperature as temperature

import Model.Device.historic as historic

import Model.Draw.draw as draw 

import Model.Place.place as place
import Model.Place.ghomeuser as ghomeuser


class ModelTest(unittest2.TestCase):

	@classmethod
	def setUpClass(self):
		connect('test')

		ghomeuser.GHomeUser.drop_collection()
		historic.Historic.drop_collection()
		ghomedevice.Device.drop_collection()
		draw.Draw.drop_collection()	
		place.Place.drop_collection()

	########################################################################
	# Tests for User base
	########################################################################
	def test_user(self):
		#Deleting pre-existing users to clean the test database
		#ghomeuser.GHomeUser.drop_collection()

		#user1
		user1 = ghomeuser.GHomeUser(name = "Dupont", password = "test", role = "Basic")
		user2 = ghomeuser.GHomeUser(name = "Martin", password = "pass", role = "Admin")

		#Adding new users
		user1.save()
		user2.save() 
		
		user1.setPassword("changed,Modafucka")
		user2.setName("Martine")

		#Invalid user: name is missing (uncomment to test)
		#user3 = ghomeuser.GHomeUser(password = "f*ck", role = "Basic")	
		#user3.save()
			
		self.assertEqual(ghomeuser.GHomeUser.objects.count(), 2)	
			
		#Printing users in Utilisateur base
		for user in ghomeuser.GHomeUser.objects:
			if user.name == "Dupont":
				self.assertEqual(user.password, "changed,Modafucka")
				self.assertEqual(user.role, "Basic")
			elif user.name == "Martine":
				self.assertEqual(user.password, "pass")
				self.assertEqual(user.role, "Admin")
			else:
				print "User name: ", user.name
				self.assertTrue(False)
	########################################################################


	########################################################################
	# Tests for Device base
	########################################################################
	def test_device(self):
		#Deleting pre-existing devices to clean the test database
		#ghomedevice.Device.drop_collection()
		
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
		
		#capteur2: temperature type, historic at creation, use addState()
		capteur2 = temperature.Temperature(physic_id = "AEFF4242", name = "CAPTEUR2_CUISINE", current_state = 22, historic = historic2)
		capteur2.save()
		capteur2.addState(datetime.datetime.now(), 27)
		
		actuator3 = actuator.Actuator(physic_id = "AEEFFA4", name = "ACTIONNEUR1_GARAGE", current_state = "CLOSED")
		actuator3.save()
		actuator3.update("OPEN")
		
		self.assertEqual(ghomedevice.Device.objects.count(), 4)

		#Print all devices' info'
		for device in ghomedevice.Device.objects:
			if device.physic_id == "12230EAF":
				self.assertEqual(device.name, "CAPTEUR1_CUISINE")
				self.assertEqual(device.current_state, 20)
				self.assertEqual(device.historic.state, [19])
			
			elif device.physic_id == "4562312AAA":
				self.assertEqual(device.name, "ACTIONNEUR2_TOILETTE")
				self.assertEqual(device.current_state, "OPEN")
				self.assertEqual(device.historic.state, [25, 22])
				
			elif device.physic_id == "AEFF4242":
				self.assertEqual(device.name, "CAPTEUR2_CUISINE")
				self.assertEqual(device.current_state, 22)
				self.assertEqual(device.historic.state, [25, 22, 27])
				
			elif device.physic_id == "AEEFFA4":
				self.assertEqual(device.name, "ACTIONNEUR1_GARAGE")
				self.assertEqual(device.current_state, "OPEN")
				self.assertEqual(device.historic.state, ["CLOSED"])
				
			else:
				print "Physic id: ", device.physic_id
				self.assertTrue(False)

		capteur1.deleteDevice()
		self.assertEqual(ghomedevice.Device.objects.count(), 3)
		self.assertEqual(historic.Historic.objects.count(), 3)
	########################################################################


	########################################################################
	# Tests for Place base
	########################################################################
	def test_place(self):
		#Deleting pre-existing draws to clean the test database
		#draw.Draw.drop_collection()	
		#place.Place.drop_collection()
		#form.Form.drop_collection()		
		
		homeDraw = draw.Draw()
		homeDraw.save()

		homeDraw.addForm("Rubiks_cube.svg")
		homeDraw.addForm("Rubiks_cube.svg")
		
		home = place.Place(name = "HOME", draw = homeDraw, maxX = 30, maxY = 30, maxZ = 6, users = [], devices = ghomedevice.Device.objects)
		home.save()
		
		for aPlace in place.Place.objects:
			if aPlace.name == "HOME":
				self.assertEqual(aPlace.maxX, 30)
				self.assertEqual(aPlace.maxY, 30)
				self.assertEqual(aPlace.maxZ, 6)
				self.assertEqual(len(aPlace.draw.form), 2)
				
				"""fo = open('test', 'w')
				fo.write(aPlace.draw.form[0].read())
				fo.close()"""

				for aUser in aPlace.users:
					print aUser.name
			
			else:
				print aPlace.name
				self.assertTrue(False)
		
		
if __name__ == '__main__':
	unittest2.main()

