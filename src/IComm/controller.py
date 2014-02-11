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

import Model.Place.place as place
import Model.Place.ghomeuser as ghomeuser

connect('test')

def getDevice(device_name):
    device = ghomedevice.Device.objects(name = device_name)[0]
    return device

# Get a device current value using its name
def getDeviceValue(device_name):
    device = getDevice(device_name = device_name)
    return device.current_state

# Add a device to the database, using its device_id, device_name and device_type
def addDevice(device_id, device_name, device_type):
    if device_type.lower() == "switch":
        newDevice = switch.Switch(physic_id = device_id, name = device_name)    
    elif device_type.lower() == "temperature":
        newDevice = temperature.Temperature(physic_id = device_id, name = device_name)
    elif device_type.lower() == "actuator":
        newDevice = actuator.Actuator(physic_id = device_id, name = device_name)
    else:
        return False

    newDevice.save()
    return True

# Delete a device, using its device_name
def deleteDevice(device_name):
    device = getDevice(device_name = device_name)
    device.deleteDevice()

# Update a device, using its device_name and the new state that has to be put in DB
def updateDevice(device_name, state):
    device = getDevice(device_name = device_name)
    device.update(stateValue = state)

# Get the form of the Place (using its place_name) which is in the list_position on the form list (default is first position)
def getForm(place_name, list_position = 0):
    default_place = place.Place.objects(name = place_name)[0]
    return default_place.draw.form[list_position]
