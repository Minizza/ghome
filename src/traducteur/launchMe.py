# -*-coding:Utf-8 -*

from traducteur.traductor import *
from mongoengine import *


addr='134.214.106.23'
port=5000

def addCaptor():
    """
    """

def main():
    connect('test')
    addCaptor()
    myTrad=traductor()
    myTrad.launch(addr,port)


if __name__ == '__main__':
    main()