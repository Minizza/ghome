# -*-coding:Utf-8 -*

from mongoengine import *
import socket
import trame

class fakePosition():

    def __init__(self):
        self.positionAbs = {'x':0, 'y':0}
        self.start = "A55A4242"
        #dataBytes
        self.ident = "12345601"
        self.end ="FF"

        #Hard Value !
        self.maxX=500
        self.maxY=500
        #Hard Value !
        self.addr=''
        self.port=1515

    def update(self,absX,absY):
        newCoord=self.translateCoord(absX,absY)
        strTrame=self.start+newCoord.get('x')+newCoord.get('y')+self.ident+self.end
        myTrame=trame.trame(strTrame)
        myTrame.calculateChecksum()
        print myTrame.lessRawView()
        self.sendTrame(myTrame.rawView())


    def translateCoord(self,absX,absY):
        """
        convert absolute coordonate to 4 Bytes value
        """
        rawConvertedX=hex(absX*(16**4-1)/self.maxX)
        rawConvertedY=hex(absY*(16**4-1)/self.maxY)
        return {'x':rawConvertedX[2:],'y':rawConvertedY[2:]}

    def sendTrame(self,trameToSend):
        """
        Create the trame from calculated cooordonates
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.addr,self.port))
        server.listen(5)  
        c,addrOut=server.accept()
        c.send(trameToSend)
        c.close

   
def main():
    blarg=fakePosition()
    blarg.update(500,500)

if __name__ == '__main__':
       main()   
