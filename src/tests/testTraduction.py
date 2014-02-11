# -*-coding:Utf-8 -*

import socket
import thread
import unittest2

import sys

"""I want da model"""
from Model.Device.device import *
from Model.Device.actuator import * 
from Model.Device.historic import *
from Model.Device.sensor import *
from Model.Device.switch import *
from Model.Device.temperature import *
    
path = "../Model/User/"
sys.path.append(path)

from user import *

path = "../traducteur"
sys.path.append(path)

from traductor import *
from fakeJerome import *

from mongoengine import *



connect('test')



def send_trameDoor():
    print "Demarrage du fauxServeur"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 1515))    
    server.listen(5)
    c,adrr = server.accept()
    print "         envoie de trame"
    c.send('A55A0B06000000090001B25E002B')

def send_trameTemp():
    print "Demarrage du fauxServeur"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 1515))    
    server.listen(5)
    c,adrr = server.accept()
    print "         envoie de trame : A55A0B07000078080089338200D0"
    c.send('A55A0B07000078080089338200D0')
    #sensor is supposed to be in da base and send temp equal to 18




class ModelTest(unittest2.TestCase):
########################################################################
    # Tests for FakeJerome trameGetting
    ########################################################################

    def setUp(self):
        #Deleting pre-existing peripherique to clean the test database
        Device.drop_collection()
        print "=============================="
         

    def tearDown(self):
        #Deleting pre-existing peripherique to clean the test database
        Device.drop_collection()
        print "le serveur meurt !"
        server.close()
        print "=============================="
    
    def test_fakeJerome(self):
        thread.start_new_thread(send_trameDoor,())
        print "Test de fake Gérome + base + traducteur" 
        capteur1 = Sensor(physic_id = "12230EAF", name = "CAPTEUR1_CUISINE", current_state = 19)
        
        capteur1.save()

        tram = trame('A55A0B06000000080001B25E002A')
        capteur = Switch(physic_id = tram.ident, name = "INTERRUPTEUR_PLAQUE", current_state = False)
        capteur.save()

        print "Base : "
        for device in Device.objects:
            print device.physic_id, " ", device.current_state

        tradMeThis = traductor()
        tradMeThis.connect('',1515)
        tradMeThis.receive()
        tradMeThis.checkTrame()

        comparedCapt = Sensor.objects(physic_id=tram.ident)[0]
        print comparedCapt.current_state

        print "Base after :"
        for device in Device.objects:
            print device.physic_id, " ", device.current_state

        self.assertTrue(comparedCapt.current_state)


    def test_temp(self):
        thread.start_new_thread(send_trameTemp,())
        print "Test capteur de température "
        capteur1 = Temperature(physic_id = "00893382", name = "CAPTEUR1_TEMP", current_state = 15)
        capteur1.save()

        assert (capteur1.physic_id in daatObj.physic_id for daatObj in Device.objects),"New sensor in Da dataBase"

        print "before"
        for device in Device.objects:
            print device.physic_id, " ", device.current_state
        tradMeThis = traductor()
        tradMeThis.connect('',1515)
        tradMeThis.receive()
        tradMeThis.checkTrame()

        print "after"
        for device in Device.objects:
            print device.physic_id, " ", device.current_state


        
########################################################################

if __name__== '__main__':
    unittest2.main()
