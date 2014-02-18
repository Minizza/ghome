# -*-coding:Utf-8 -*

from traducteur.traductor import *
from mongoengine import *


addr=''
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