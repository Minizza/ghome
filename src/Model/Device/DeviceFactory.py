
from temperature import *
from switch import *
from position import *
from actuator import *
from device import *

class DeviceFactory(object):

    @staticmethod
    def newDevice(type, physic_id, name):
        if type == "temperature":
            new = Temperature(x=Device.UNDEFINED_COORDINATE, y=Device.UNDEFINED_COORDINATE, physic_id=physic_id, name=name)
        elif type == "switch":
            new = Switch(x=Device.UNDEFINED_COORDINATE, y=Device.UNDEFINED_COORDINATE, physic_id=physic_id, name=name)
        elif type == "position":
            new = Position(x=Device.UNDEFINED_COORDINATE, y=Device.UNDEFINED_COORDINATE, physic_id=physic_id, name=name)
        elif type == "actuator":
            new = Actuator(x=Device.UNDEFINED_COORDINATE, y=Device.UNDEFINED_COORDINATE, physic_id=physic_id, name=name)
        else:
            raise TypeError("Bad device creation, type " + type + " doesn't exist !")
        return new

    @staticmethod
    def getTypes():#Nom du type => nom de presentation
        return [('temperature','Temperature'),('switch','Switch'),('position','Position'), ('actuator', 'Actuator')]
