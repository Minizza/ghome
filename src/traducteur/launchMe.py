# -*-coding:Utf-8 -*

from traducteur.traductor import *
from mongoengine import *

#fichier de conf
from IComm.server import CONFIG


def main():
    connect('test')
    myTrad=traductor().launch(CONFIG['platforme'],CONFIG['platformePort'])


if __name__ == '__main__':
    main()