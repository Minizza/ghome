# -*- coding : utf-8 -*-

import socket
import pygame
from pygame.locals import *

#Initialyzing pygame
pygame.init()

#Creation of the window
window = pygame.display.set_mode((800,600))

#chargement du fond
backG = pygame.image.load("medias/fond.png")
window.blit(backG,(0,0))

#mise en place des capteurs
capt1 = pygame.image.load("medias/capt.png")
pos_capt1 = window.blit(capt1,(100,100))

capt2 = pygame.image.load("medias/capt.png")
pos_capt2 = window.blit(capt1,(500,300))

capt3 = pygame.image.load("medias/capt.png")
pos_capt3 = window.blit(capt1,(400,500))

#Shut down the application (sd==1 -> continue / sd==0 -> close)
sd = 1

while sd:
	#on rafraichit l'ecran
	pygame.display.flip()

	#on teste les events
	for event in pygame.event.get():
		if event.type == QUIT:
			sd = 0
		if event.type == MOUSEBUTTONDOWN and event.button == 1:
			x,y = event.pos
			if pos_capt1.collidepoint(x,y):
				print "capt1 !!!"
			elif pos_capt2.collidepoint(x,y):
				print "capt2 !!!"
			elif pos_capt3.collidepoint(x,y):
				print "capt3 !!!"
			else : 
				print "oulougoulouglou"