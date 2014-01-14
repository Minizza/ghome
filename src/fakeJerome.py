from pants import Engine, Server, Stream

class Echo(Stream):
    def on_read(self, data):
        self.write(data)
    def balancer(data):
        self.write(data)


def main () :
    print 'fakeJerome : concepteur de fakeTrames'
    while 1 : 
        print 'Que voulez vous balancer ? (tavu ?)\n'
        print '1 : Capteur température \n'
        print '2 : Capteur contact'
        print '3 : Capteur présence'
        kloug = raw_input()
        print kloug

main()    
