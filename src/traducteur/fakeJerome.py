# -*- coding : utf-8 -*-

import socket
import time
import atexit
from random import randrange
"""
fakeJerome est un simple support d'envoi de fausses trames pour tester
sans avoir de capteur sous la main
"""

server = socket.socket()


def balTemp (c):
    data = 'A55A0B06000000080001B25E002A'
    print "Sending : {}".format(data)
    c.send(data)

def balCont (c):
    data = 'A55A0B07A830000F00053F440081'
    print "Sending : {}".format(data)
    c.send(data)

def balPres (c):
    data = 'A55A0B079DB8000D0004E59500F2'
    print "Sending : {}".format(data)
    c.send(data)

def auto () :
    print 'fakeJerome : concepteur de fakeTrames'
    print 'Auto mode : send random trames every 5s'
    chan = server.bind(('', 1515))    
    server.listen(10000)  
    c,adrr = server.accept()      
    while 1 : 
        test = randrange(1,3)
        if test == 1 :
            balTemp(c)
        elif test == 2 :
            balCont(c)
        elif test == 3 :
            balPres(c)
        else : 
            raise Exception("random out of bounds")
        time.sleep(5)

def manual () :
    print 'fakeJerome : concepteur de fakeTrames'
    print 'Manual mode'
    chan = server.bind(('', 1515))    
    server.listen(10000)  
    c,adrr = server.accept()      
    while 1 : 
        print 'Que voulez vous balancer ? (tavu ?)\n'
        print '1 : Capteur temperature'
        print '2 : Capteur contact'
        print '3 : Capteur presence'
        kloug = raw_input('A vous :')
        test = int(kloug)
        if test == 1 :
            balTemp(c)
        elif test == 2 :
            balCont(c)
        elif test == 3 :
            balPres(c)
        else : 
            print 'Haha petit malin !'

def servClose():
	print "le serveur meurt !"
	server.close()

atexit.register(servClose)

if __name__ == '__main__':
	"Choose ONE mode"
	manual()
	#auto() 
	print "le serveur meurt !"
	server.close()

