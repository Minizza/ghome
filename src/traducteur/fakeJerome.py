# -*- coding : utf-8 -*-

import socket
import atexit
# from IComm.server import CONFIG
"""
fakeJerome est un simple support d'envoi de fausses trames pour tester
sans avoir de capteur sous la main
"""




def balTemp (c):
    data = 'A55A0B07A830000800053F44007A'
    print "Sending : {}".format(data)
    c.send(data)

def balCont (c):
    data = 'A55A0B07A830000900053F44007B'
    print "Sending : {}".format(data)
    c.send(data)

def balPres (c):
    data = 'A55A0B079DB8000D0004E59500F2'
    print "Sending : {}".format(data)
    c.send(data)

def balBad (c):
    data = 'A55A0B079DB8000D0004E59500F5'
    print "Sending : {}".format(data)
    c.send(data)


def manual () :
    print 'fakeJerome : concepteur de fakeTrames'
    print 'Manual mode'
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.connect(('', 1515))
    while 1 : 
        print 'Que voulez vous balancer ? (tavu ?)\n'
        print '1 : Capteur temperature'
        print '2 : Capteur contact'
        print '3 : Capteur presence'
        print '4 : mauvaisse trame'
        kloug = raw_input('A vous :')
        test = int(kloug)
        if test == 1 :
            balTemp(server)
        elif test == 2 :
            balCont(server)
        elif test == 3 :
            balPres(server)
        elif test==4:
            balBad(server)
        else : 
            print 'Haha petit malin !'

def servClose():
    print "le serveur meurt !"
    server.close()

atexit.register(servClose)

if __name__ == '__main__':
    manual()