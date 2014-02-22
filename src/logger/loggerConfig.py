#!/usr/bin/env python
# -*- coding: utf-8 -*-
 

 #piqué sur sam & max pour les détails voir http://sametmax.com/ecrire-des-logs-
 #en-python/ 
import logging
import sys
import inspect

from loggerColor import *
 
from logging.handlers import RotatingFileHandler 
def configure ():
	"""
	Configure the logging system to keep a trace of everything both in console and log file
	"""
	# création de l'objet logger qui va nous servir à écrire dans les logs
	logger = logging.getLogger()
	# on met le niveau du logger à DEBUG, comme ça il écrit tout
	logger.setLevel(logging.DEBUG)


	###############Ecrit dans un fichier
	# création d'un formateur qui va ajouter le temps, le niveau
	# de chaque message quand on écrira un message dans le log
	formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
	# création d'un handler qui va rediriger une écriture du log vers
	# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
	file_handler = RotatingFileHandler('../../log/activity.log', 'a', 1000000, 1)
	# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
	# créé précédement et on ajoute ce handler au logger
	file_handler.setLevel(logging.INFO)
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	 

	##########Dans la console
	# création d'un second handler qui va rediriger chaque écriture de log
	# sur la console
	# steam_handler = logging.StreamHandler()
	# consolFormat = logging.Formatter('%(levelname)s :: %(message)s')
	# steam_handler.setFormatter(consolFormat)
	# #niveau de début
	# steam_handler.setLevel(logging.DEBUG)
	# logger.addHandler(steam_handler)

	steam_handler = RainbowLoggingHandler(sys.stdout)
	consolFormat = logging.Formatter('%(levelname)s :: %(message)s')
	steam_handler.setFormatter(consolFormat)
	#niveau de début
	steam_handler.setLevel(logging.DEBUG)
	logger.addHandler(steam_handler)
	curframe = inspect.currentframe()
	calframe = inspect.getouterframes(curframe, 2)
	logger.info("A new logger is born from {}".format(calframe[1][3]))
	return logger