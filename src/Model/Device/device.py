# -*-coding:Utf-8 -*

from mongoengine import *
from historic import *

import datetime


class Device(Document):
    """Classe mère pour les périphériques
        - id : l'id du périphérique dans l'application
        - id_physique : l'id physique du périphérique
        - historique : l'historique des états du périphérique
        - etat_courant : l'état courant du périphérique"""
        
    meta = {'allow_inheritance': True} #Autorise l'héritage de cette classe
        
    id = ObjectIdField(required = True)
    physic_id = StringField(required = True, unique = True)
    name = StringField(required = True, unique = True)
    historic = ReferenceField(Historic)
    current_state = DynamicField()
    coordX = IntField()
    coordY = IntField()
    coordZ = IntField()
    
    def setHistoric(self, historicValue):
        historicValue.save()
        self.historic = historicValue
        self.save()
        
    def setCurrentState(self, state):
        self.current_state = state
        self.save()
    
    def addState(self, stateDate, stateValue):
        if not(self.historic):      #If the histic does not exist
            self.historic = Historic(date = [stateDate], state = [stateValue])
        else:
            self.historic.date.append(stateDate)
            self.historic.state.append(stateValue)
        self.historic.save()
        
    def update(self, stateValue):
        self.addState(datetime.datetime.now(), self.current_state)
        self.setCurrentState(stateValue)
