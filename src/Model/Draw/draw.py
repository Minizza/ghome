# -*-coding:Utf-8 -*

from mongoengine import *
from form import *

class Draw(Document):
		
	id = ObjectIdField(required = True) # Id requis
	form = ListField(ReferenceField(Form))
	
