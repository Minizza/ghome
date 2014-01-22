# -*-coding:Utf-8 -*

from mongoengine import *


class GHomeUser(Document):
	"""Utilisateur de l'application
		- id : l'id de l'utilisateur
		- nom : nom de l'utilisateur
		- mdp : mot de passe de l'utilisateur
		- role : rôle de l'utilisateur"""
		
	id = ObjectIdField(required = True) # Id requis
	name = StringField(max_length = 20, required = True) # Taille max : 20 caractères
	password = StringField(max_length = 20, required = True) # Taille max : 20 caractères
	role = StringField(required = True)