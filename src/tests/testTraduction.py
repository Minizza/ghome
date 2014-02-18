# -*-coding:Utf-8 -*

import socket
import thread
import unittest2
import colorama
import time

"""I want da model"""
from Model.Device.device import *
from Model.Device.actuator import * 
from Model.Device.historic import *
from Model.Device.sensor import *
from Model.Device.switch import *
from Model.Device.temperature import *    

from traducteur.traductor import *
from traducteur.trame import *

from mongoengine import *






def send_trameDoor():
    tramounette = 'A55A0B06000000090001B25E002B'
    print "Demarrage du fauxServeur"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 1515))    
    server.listen(5)
    c,adrr = server.accept()
    print "         envoie de trame : {}".format(tramounette)
    c.send(tramounette)
    server.close()

def send_trameTemp():
    tramounette = 'A55A0B07000078080089338200D0'
    print "Demarrage du fauxServeur"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 1515))    
    server.listen(5)
    c,adrr = server.accept()
    print "         envoie de trame : {}".format(tramounette)
    c.send(tramounette)
    #sensor is supposed to be in da base and send temp equal to 18
    server.close()



class ModelTest(unittest2.TestCase):
########################################################################
    # Tests for FakeJerome trameGetting
    ########################################################################

    def setUp(self):
        connect('test')
        #Deleting pre-existing peripherique to clean the test database
        Device.drop_collection()
        print ("==============================Début")
         

    def tearDown(self):
        #Deleting pre-existing peripherique to clean the test database
        Device.drop_collection()
        print "==============================Fin"
    
    def test_fakeJerome(self):
        thread.start_new_thread(send_trameDoor,())
        print (colorama.Fore.GREEN+"     Test de fake Gérome + base + traducteur"+colorama.Fore.RESET)
        capteur1 = Sensor(physic_id = "12230EAF", name = "CAPTEUR1_CUISINE", current_state = 19)
        
        capteur1.save()

        tram = trame('A55A0B06000000080001B25E002A')
        capteur = Switch(physic_id = tram.ident, name = "INTERRUPTEUR_PLAQUE", current_state = False)
        capteur.save()

        print (colorama.Fore.MAGENTA + "Base : "+colorama.Fore.RESET)
        for device in Device.objects:
            print (colorama.Fore.MAGENTA +"{} {}"+colorama.Fore.RESET).format(device.physic_id, device.current_state)
        tradMeThis = traductor()
        # tradMeThis.connect('',1515)
        # tradMeThis.receive()
        # tradMeThis.checkTrame()
        tradMeThis.launch('',1515)
        
        #Pourquoi de voir attendre !!!! 
        time.sleep(0.1)

        comparedCapt = Sensor.objects(physic_id=tram.ident)[0]
        print comparedCapt.current_state

        print (colorama.Fore.MAGENTA + "Base after: "+colorama.Fore.RESET)
        for device in Device.objects:
            print (colorama.Fore.MAGENTA +"{} {}"+colorama.Fore.RESET).format(device.physic_id, device.current_state)

        print "                     ARRET"
        tradMeThis.stop()
        self.assertTrue(comparedCapt.current_state)


    def test_temp(self):
        thread.start_new_thread(send_trameTemp,())
        print (colorama.Fore.GREEN+"     Test capteur de température "+colorama.Fore.RESET)
        capteur1 = Temperature(physic_id = "00893382", name = "CAPTEUR1_TEMP", current_state = 15)
        capteur1.save()

        assert (capteur1.physic_id in daatObj.physic_id for daatObj in Device.objects),"New sensor in Da dataBase"

        print (colorama.Fore.MAGENTA + "Base before: "+colorama.Fore.RESET)
        for device in Device.objects:
            print (colorama.Fore.MAGENTA +"{} {}"+colorama.Fore.RESET).format(device.physic_id, device.current_state)

        tradMeThis = traductor()
        # tradMeThis.connect('',1515)
        # tradMeThis.receive()
        # tradMeThis.checkTrame()
        tradMeThis.launch('',1515)

        #Pourquoi de voir attendre !!!! 
        time.sleep(0.1)

        print (colorama.Fore.MAGENTA + "Base after : "+colorama.Fore.RESET)
        for device in Device.objects:
            print (colorama.Fore.MAGENTA +"{} {}"+colorama.Fore.RESET).format(device.physic_id, device.current_state)
        tradMeThis.stop()
        capteur1=Sensor.objects(physic_id = "00893382")[0]
        self.assertAlmostEqual(capteur1.current_state, 18.82, places=2)

        
########################################################################

if __name__== '__main__':
    unittest2.main()
