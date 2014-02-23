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
	pClient = Process(target = runserver.main)
	pTrad = Process(target = launchMe.main)

	# Process can be launch without the main one
	pClient.daemon = True
	pTrad.daemon = True

	# Start new process
	pClient.start()
	pTrad.start()

	# Wainting for both process to end
	pTrad.join()
	pClient.join()

if __name__ == '__main__':
    main()