# -*-coding:Utf-8 -*

from mongoengine import *
import Trame
from Model.Device import position
from logger import LOGGER


class fakePosition():

    def __init__(self,player):
        self.start = player.trameStart
        #dataBytes
        self.ident = player.physic_id
        self.end =player.trameEnd
        self.maxX=player.maxX
        self.maxY=player.maxY


    def update(self,absX,absY):
        newCoord=self.translateCoord(absX,absY)
        strTrame=self.start+newCoord.get('x')+newCoord.get('y')+self.ident+self.end
        myTrame=Trame.trame(strTrame)
        myTrame.calculateChecksum()
        LOGGER.debug("Frame to be send : {}".format(myTrame.lessRawView()))





   
def main():
    player11 = position.Position(physic_id = "ADEDF3E7", name = "Equipe 1 joueur 1", current_state = {"coordX":50,"coordY":500}, coordX = 50, coordY = 500)
    blarg=fakePosition(player11)
    blarg.update(610,545)

if __name__ == '__main__':
       main()   
