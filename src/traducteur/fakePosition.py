# -*-coding:Utf-8 -*

from mongoengine import *
import socket
import trame
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

        #Hard Value !
        self.addr='134.214.106.23'
        self.port=5000

    def update(self,absX,absY):
        newCoord=self.translateCoord(absX,absY)
        strTrame=self.start+newCoord.get('x')+newCoord.get('y')+self.ident+self.end
        myTrame=trame.trame(strTrame)
        myTrame.calculateChecksum()
        LOGGER.debug("Frame to be send : {}".format(myTrame.lessRawView()))
        self.sendTrame(myTrame.rawView())


    def translateCoord(self,absX,absY):
        """
        convert absolute coordonate to 4 Bytes value
        """
        rawConvertedX=hex(absX*(16**4-1)/self.maxX).upper()
        rawConvertedY=hex(absY*(16**4-1)/self.maxY).upper()
        return {'x':rawConvertedX[2:],'y':rawConvertedY[2:]}

    def sendTrame(self,trameToSend):
        """
        Create the trame from calculated cooordonates
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server=socket.socket()
        server.connect((self.addr,self.port))
        server.send(trameToSend)
        LOGGER.info("Trame to send : {}".format(trameToSend))
        server.close()

   
def main():
    player11 = position.Position(physic_id = "ADEDF3E7", name = "Equipe 1 joueur 1", current_state = {"coordX":50,"coordY":500}, coordX = 50, coordY = 500)
    blarg=fakePosition(player11)
    blarg.update(610,545)

if __name__ == '__main__':
       main()   
