# -*- coding : utf-8 -*-

from pants import Engine, Server, Stream

class Echo(Stream):
    def on_read(self, data):
        self.write(data)
    def balancer(self,data):
        self.write(data)


server = Server(ConnectionClass=Echo)

def balTemp ():
    data = 'A55A0B06000000080001B25E002A'
    server.on_read(data)

def balCont ():
    data = 'A55A0B07A830000F00053F440081'
    server.on_read(data)

def balPres ():
    data = 'A55A0B079DB8000D0004E59500F2'
    server.on_read(data)

def main () :
    print 'fakeJerome : concepteur de fakeTrames'
    while 1 : 
        print 'Que voulez vous balancer ? (tavu ?)\n'
        print '1 : Capteur temperature'
        print '2 : Capteur contact'
        print '3 : Capteur presence'
        kloug = raw_input('A vous :')
        test = int(kloug)
        if test == 1 :
            balTemp()
        elif test == 2 :
            balCont()
        elif test == 3 :
            balPres()
        else : 
            print 'Haha petit malin !'

main()    
