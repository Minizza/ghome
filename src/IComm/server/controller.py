#!/usr/bin/env python
# -*-coding:Utf-8 -*

from server import app

from mongoengine import *

import sys

import Model.Device.DeviceFactory as factory

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

# Return a device using its device_name
def getDevice(device_name):
    device = ghomedevice.Device.objects(name = device_name)[0]
    return device

# Return a place using its place_name
def getPlace(place_name):
    default_place = place.Place.objects(name = place_name)[0]
    return default_place

# Get a device current value using its name
def getDeviceValue(device_name):
    device = getDevice(device_name = device_name)
    return device.current_state

# Add a device to the database, using its device_id, device_name and device_type
def addDevice(device_type, device_id, device_name,):
    device = factory.DeviceFactory.newDevice(device_type.lower(), device_id, device_name)
    device.save()

# Create a new place with a place_name
def addPlace(place_name):
    newPlace = place.Place(name = place_name)
    newPlace.save()

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
    default_place = getPlace(place_name = place_name)
    return default_place.draw.form[list_position]

# Save a file (identified by its file_name) into a place (identified by its place_name)
def saveForm(place_name, file_name):
    default_place = getPlace(place_name = place_name)
    default_place.addForm(file_name)

# Fetch all devices
def fetchDevices():
    devices = ghomedevice.Device.objects # Fetch les devices depuis la BD ici !
    for device in devices:
        device.type = type(device).__name__
    return devices