# -*-coding:Utf-8 -*

from traducteur.traductor import *
from mongoengine import *


addr=''
port=1515

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