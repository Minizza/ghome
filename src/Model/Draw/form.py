# -*-coding:Utf-8 -*

from mongoengine import *

class Form(Document):
		
	id = ObjectIdField(required = True) # Id requis
	coordX = ListField(IntField())
	coordY = ListField(IntField())
	coordZ = IntField()
	
