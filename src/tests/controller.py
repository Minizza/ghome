# -*-coding:Utf-8 -*

from mongoengine import *

import sys
import datetime

import unittest2

import tests.model as model_test

import IComm.controller as controller

import Model.Device.device as ghomedevice

import Model.Device.sensor as sensor
import Model.Device.actuator as actuator
import Model.Device.temperature as temperature

import Model.Device.historic as historic

import Model.Draw.draw as draw 
import Model.Draw.form as form

import Model.Place.place as place
import Model.Place.ghomeuser as ghomeuser


class ModelTest(unittest2.TestCase):

	@classmethod
	def setUpClass(self):
		connect('test')
		ghomedevice.Device.drop_collection()


	def test(self):
		#Setting a date field and a state field
		dateField = [datetime.datetime.now(), datetime.datetime.now()]
		stateField = [25, 22]
		
		#capteur1: no historic at creation, uses add_state() and setCurrentState()	
		capteur1 = sensor.Sensor(physic_id = "12230EAF", name = "CAPTEUR1_CUISINE", current_state = 19)
		capteur1.save()
		capteur1.addState(datetime.datetime.now(), capteur1.current_state)
		capteur1.setCurrentState(20)	

		device_cuisine = ghomedevice.Device.objects(physic_id = "12230EAF")[0]
		self.assertEqual(controller.getDeviceValue("CAPTEUR1_CUISINE"), device_cuisine.current_state)

		controller.addDevice(device_id = "AE2R44", device_name = "SWITCH1_ENTREE", device_type = "SWITCH")
		device_switch = ghomedevice.Device.objects(physic_id = "AE2R44")[0]
		#device_switch.update(True)

		controller.updateDevice(device_name = "SWITCH1_ENTREE", state = True)

		self.assertEqual(controller.getDeviceValue("SWITCH1_ENTREE"), True)

		controller.deleteDevice(device_name = "SWITCH1_ENTREE")
		self.assertEqual(ghomedevice.Device.objects.count(), 1)


if __name__ == '__main__':
	unittest2.main()
 