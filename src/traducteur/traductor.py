#!/usr/bin/python
# -*- coding: utf-8 -*-
          

from pants import Engine, Server, Stream


class Echo(Stream):
    def on_read(self, data):
        self.write(data)




if __name__ == '__main__':
    print ("Début")
    server = Server(ConnectionClass=Echo)
    server.listen(4040)
    Engine.instance().start()