# -*-coding:Utf-8 -*

from mongoengine import *
import trame

class fakePosition():

    def __init__(self):
        self.positionAbs = {'x':0, 'y':0}
        self.maxX=500
        self.maxY=500
        self.start = "A55A4242"
        #dataBytes
        self.ident = "12345601"
        self.end ="FF"

    def update(self,absX,absY):
        newCoord=self.translateCoord(absX,absY)
        strTrame=self.start+newCoord.get('x')+newCoord.get('y')+self.ident+self.end
        print strTrame
        myTrame=trame.trame(strTrame)


    def translateCoord(self,absX,absY):
        """
        convert absolute coordonate to 4 Bytes value
        """
        rawConvertedX=hex(absX*(16**4-1)/self.maxX)
        rawConvertedY=hex(absY*(16**4-1)/self.maxY)
        return {'x':rawConvertedX[2:],'y':rawConvertedY[2:]}

    def sendTrame():
        """
        Create the trame from calculated cooordonates
        """
   
def main():
    blarg=fakePosition()
    blarg.update(500,500)

if __name__ == '__main__':
       main()   
