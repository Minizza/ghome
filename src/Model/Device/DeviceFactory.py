
from temperature import *
from switch import *

class DeviceFactory(object):

    @staticmethod
    def newDevice(type, physic_id, name):
        if type == "temperature":
            new = Temperature(physic_id=physic_id, name=name)
        elif type == "switch":
            new = Switch(physic_id=physic_id, name=name)
        else:
            "Bad device creation, type " + type + " doesn't exist !"
        return new
