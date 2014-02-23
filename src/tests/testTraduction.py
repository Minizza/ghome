# -*-coding:Utf-8 -*

import socket
import thread
import unittest2
import colorama

"""I want da model"""
from Model.Device.device import *
from Model.Device.actuator import * 
from Model.Device.historic import *
from Model.Device.sensor import *
from Model.Device.switch import *
from Model.Device.temperature import *  
from Model.update import lazzyUpdate  

from traducteur.traductor import *
from traducteur.trame import *
from traducteur.fakePosition import *
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

def send_tramePosition(player):
        fakePosition(player).update(610,545)


class ModelTest(unittest2.TestCase):
########################################################################
    # Tests for FakeJerome trameGetting
    ########################################################################

    def setUp(self):
        connect('test')
        #Deleting pre-existing peripherique to clean the test database
        Device.drop_collection()
        lazzyUpdate.drop_collection()
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

        tram = trame.trame('A55A0B06000000080001B25E002A')
        capteur2 = Switch(physic_id = tram.ident, name = "INTERRUPTEUR_PLAQUE", current_state = "close")
        capteur2.save()

        print (colorama.Fore.MAGENTA + "Base : "+colorama.Fore.RESET)
        for device in Device.objects:
            print (colorama.Fore.MAGENTA +"{} {}"+colorama.Fore.RESET).format(device.physic_id, device.current_state)
        tradMeThis = traductor()
        tradMeThis.connect('',1515)
        tradMeThis.receive()
        tradMeThis.checkTrame()


        comparedCapt = Sensor.objects(physic_id=tram.ident)[0]
        print comparedCapt.current_state

        print (colorama.Fore.MAGENTA + "Base after: "+colorama.Fore.RESET)
        for device in Device.objects:
            print (colorama.Fore.MAGENTA +"{} {}"+colorama.Fore.RESET).format(device.physic_id, device.current_state)

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
        tradMeThis.connect('',1515)
        tradMeThis.receive()
        tradMeThis.checkTrame()


        print (colorama.Fore.MAGENTA + "Base after : "+colorama.Fore.RESET)
        for device in Device.objects:
            print (colorama.Fore.MAGENTA +"{} {}"+colorama.Fore.RESET).format(device.physic_id, device.current_state)
        capteur1=Sensor.objects(physic_id = "00893382")[0]
        self.assertAlmostEqual(capteur1.current_state, 18.82, places=2)



    def test_UpdateTradsensorSet(self):
        print (colorama.Fore.GREEN+"     Test de lazzyUpdate"+colorama.Fore.RESET)
        capteur1 = Temperature(physic_id = "01234567", name = "CAPTEUR1_TEMP", current_state = 15)
        capteur1.save()

        tradMeThis = traductor()
        self.assertIn("01234567",tradMeThis.identSet,msg="Pas trouvé ")


        capteur2 = Switch(physic_id = "98765432", name = "INTERRUPTEUR_PLAQUE", current_state = "close")
        capteur2.save()
        
        lazzyUpdate().updateAll()
        self.assertIn("01234567",tradMeThis.identSet,msg="Pas trouvé ")
        self.assertNotIn("98765432",tradMeThis.identSet,msg="Pas trouvé ")
        tradMeThis.updateIdentSet()
        self.assertIn("98765432",tradMeThis.identSet,msg="Pas trouvé ")


    # def test_position(self):
    #     print (colorama.Fore.GREEN+"     Test de faux capteur de position"+colorama.Fore.RESET)
    #     player11 = position.Position(physic_id = "ADEDF3E7", name = "Equipe 1 joueur 1", current_state = {"coordX":50,"coordY":500}, coordX = 50, coordY = 500)
    #     player11.save()

    #     print (colorama.Fore.MAGENTA + "Base before: "+colorama.Fore.RESET)
    #     for device in Device.objects:
    #         print (colorama.Fore.MAGENTA +"{} {}"+colorama.Fore.RESET).format(device.physic_id, device.current_state)

    #     mytrad=traductor()
    #     mytrad.connect('134.214.106.23',5000)
    #     fakePosition(player11).update(608,545)
    #     thread.start_new_thread(send_tramePosition,(player11,))
    #     mytrad.receive()
    #     mytrad.checkTrame()

    #     print (colorama.Fore.MAGENTA + "Base after: "+colorama.Fore.RESET)
    #     for device in Device.objects:
    #         print (colorama.Fore.MAGENTA +"{} {}"+colorama.Fore.RESET).format(device.physic_id, device.current_state)

        
########################################################################

if __name__== '__main__':
    unittest2.main()
