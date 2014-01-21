# -*-coding:Utf-8 -*

from mongoengine import *

import sys
import ghomeuser

path = "../Device/"
if path not in sys.path:
	sys.path.append(path)

import device

path = "../Draw/"
if path not in sys.path:
	sys.path.append(path)

import draw


class Place(Document):
		
	id = ObjectIdField(required = True) # Id requis
	name = StringField(max_length = 20, required = True)
	draw = ReferenceField(draw.Draw)
	maxX = IntField()
	maxY = IntField()
	maxZ = IntField()
	users = ListField(ReferenceField(ghomeuser.GHomeUser))
	devices = ListField(ReferenceField(device.Device))
	
