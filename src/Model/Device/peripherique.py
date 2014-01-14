# -*-coding:Utf-8 -*

from mongoengine import *
from historique import *


class Peripherique(Document):
    """Classe mère pour les périphériques
        - id_logique : l'id du périphérique dans l'application
        - id_physique : l'id physique du périphérique
        - historique : l'historique des états du périphérique
        - etat_courant : l'état courant du périphérique"""
        
    meta = {'allow_inheritance': True} #Autorise l'héritage de cette classe
        
    id_logique = ObjectIdField(required = True)
    id_physique = StringField(required = True)
    historique = ReferenceField(Historique)
    etat_courant = DynamicField()
