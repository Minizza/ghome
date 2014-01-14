# -*-coding:Utf-8 -*

from mongoengine import *

class Utilisateur(Document):
	"""Utilisateur de l'application
		- id : l'id de l'utilisateur
		- nom : nom de l'utilisateur
		- mdp : mot de passe de l'utilisateur
		- role : rôle de l'utilisateur"""
		
	id = IntField(required = True) # Id requis
	nom = StringField(max_length = 20, required = True) # Taille max : 20 caractères
	mdp = StringField(max_length = 20, required = True) # Taille max : 20 caractères
	role = StringField(required = True)
