# -*-coding:Utf-8 -*

from mongoengine import *

import sys
import ghomeuser

path = "../Model/Device/"
if path not in sys.path:
	sys.path.append(path)

path = "../Model/Draw/"
if path not in sys.path:
	sys.path.append(path)

from device import *
from draw import *


class Place(Document):
		
	id = ObjectIdField(required = True) # Id requis
	name = StringField(max_length = 20, required = True)
	draw = ReferenceField(Draw)
	maxX = IntField()
	maxY = IntField()
	maxZ = IntField()
	users = ListField(ReferenceField(ghomeuser.GHomeUser))
	devices = ListField(ReferenceField(Device))
	
