# -*-coding:Utf-8 -*

from mongoengine import *
from IComm.server import app, CONFIG
from multiprocessing import Process

import traducteur.launchMe as launchMe
import runserver as runserver

database = CONFIG["database"]

connect(database)

def main():

	# Create new threads
	pClient = Process(target = runserver.main())
	print "F*ck you too!"
	pTrad = Process(target = launchMe.main())
	print "F*ck you!"

	# Start new Threads
	pClient.start()
	print "Client lancé"
	pTrad.start()
	print "Bite cul chatte"

	pTrad.join()
	print "Fin de trad"
	pClient.join()
	print "Fin de client"

if __name__ == '__main__':
    main()