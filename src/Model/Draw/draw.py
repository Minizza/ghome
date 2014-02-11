# -*-coding:Utf-8 -*

from mongoengine import *
from mongoengine import fields

import os

class Draw(Document):
        
    id = ObjectIdField(required = True) # Id requis
    form = ListField(FileField())


    def addForm(self, file_name):
        f = fields.GridFSProxy()
        to_read = open(file_name, 'r')
        f.put(to_read, filename = os.path.basename(to_read.name))

        if not(self.form):      #If the form does not exist
            self.form = [f]
        else:
            self.form.append(f)
        self.save() 
        to_read.close()
