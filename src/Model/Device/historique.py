# -*-coding:Utf-8 -*

from mongoengine import *

class Historique(Document):
	"""Classe mère pour les périphériques
			- date : la liste des dates de mesure des états du périphérique
			- etat : la liste des états du périphériques"""
