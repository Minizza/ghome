# -*-coding:Utf-8 -*

from mongoengine import *

import sys
import ghomeuser
import Model.Device.device as device
import Model.Draw.draw as ghomedraw


class Place(Document):
		
	id = ObjectIdField(required = True) # Id requis
	name = StringField(max_length = 20, required = True)
	draw = ReferenceField(ghomedraw.Draw)
	maxX = IntField()
	maxY = IntField()
	maxZ = IntField()
	users = ListField(ReferenceField(ghomeuser.GHomeUser))
	devices = ListField(ReferenceField(device.Device))

	def addForm(self, file_name):
		if not (self.draw):
			aDraw = ghomedraw.Draw()
			aDraw.save()
			self.draw = aDraw
			self.save()
			
		self.draw.addForm(file_name = file_name)
	
