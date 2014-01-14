# -*- coding : utf-8 -*-

from pants import Engine, Server, Stream

class Echo(Stream):
    def on_read(self, data):
        self.write(data)
    def balancer(data):
        self.write(data)

def balTemp ():
    data = 'A55A'
    Stream.balancer(data)

def balCont ():
    data = 'A55A'

def balPres ():
    data = 'A55A'

def main () :
    print 'fakeJerome : concepteur de fakeTrames'
    while 1 : 
        print 'Que voulez vous balancer ? (tavu ?)\n'
        print '1 : Capteur temperature'
        print '2 : Capteur contact'
        print '3 : Capteur presence'
        kloug = raw_input('A vous :')
        if 1 in kloug :
            balTemp()
        elif 2 in kloug :
            balCont()
        elif 3 in kloug :
            balPres()
        else : 
            print 'Haha petit malin !'

main()    
