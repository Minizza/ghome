# -*- coding : utf-8 -*-

import socket
import atexit
# from IComm.server import CONFIG
"""
fakeJerome est un simple support d'envoi de fausses trames pour tester
sans avoir de capteur sous la main
"""




def balOpen (c):
    data = 'A55A0B07A830000800053F44007A'
    print "Sending : {}".format(data)
    c.send(data)

def balClose (c):
    data = 'A55A0B07A830000900053F44007B'
    print "Sending : {}".format(data)
    c.send(data)

def balTemp (c):
    data = 'A55A0B070000DF08A23F45070026'
    print "Sending : {}".format(data)
    c.send(data)

def balBad (c):
    data = 'A55A0B079DB8000D0004E59500F5'
    print "Sending : {}".format(data)
    c.send(data)

def balPos(c):
    data = 'A55A424253EE53EEADEDF3E7FF79'
    print "Sending : {}".format(data)
    c.send(data)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def manual () :
    print 'fakeJerome : concepteur de fakeTrames'
    print 'Manual mode'
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.connect(('', 1515))
    while 1 : 
        print 'Que voulez vous balancer ? (tavu ?)\n'
        print '1 : Switch open'
        print '2 : Switch close'
        print '3 : Capteur temperature 35'
        print '4 : mauvaisse trame'
        print "5 : Deplacement d'un joueur"
        kloug = raw_input('A vous :')
        test = int(kloug)
        if test == 1 :
            balOpen(server)
        elif test == 2 :
            balClose(server)
        elif test == 3 :
            balTemp(server)
        elif test==4:
            balBad(server)
        elif test==5:
            balPos(server)
        else : 
            print 'Haha petit malin !'

def servClose():
    print "le serveur meurt !"
    server.close()

atexit.register(servClose)

if __name__ == '__main__':
    manual()