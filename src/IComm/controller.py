#!/usr/bin/env python
# -*-coding:Utf-8 -*

from mongoengine import *

import sys

import Model.Device.device as ghomedevice

import Model.Device.sensor as sensor
import Model.Device.actuator as actuator
import Model.Device.temperature as temperature
import Model.Device.switch as switch

import Model.Device.historic as historic

import Model.Draw.draw as draw 
import Model.Draw.form as form

import Model.Place.place as place
import Model.Place.ghomeuser as ghomeuser

connect('test')

# Get a device current value using its name
def getDeviceValue(device_name):
    device = ghomedevice.Device.objects(name = device_name)[0]
    return device.current_state

# Add a device to the database, using its device_id, device_name and device_type
def addDevice(device_id, device_name, device_type):
    if device_type.lower() == "switch":
        newDevice = switch.Switch(physic_id = device_id, name = device_name)    
    elif device_type.lower() == "temperature":
        newDevice = temperature.Temperature(physic_id = device_id, name = device_name)
    else:
        return False

    newDevice.save()
    return True