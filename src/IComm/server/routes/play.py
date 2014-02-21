#!/usr/bin/env python
# -*-coding:Utf-8 -*

import time

from server import app
from flask import render_template, request
from server.roles import *
import json
from mongoengine import *
import Model.Device.device as ghomedevice
import Model.Device.temperature as ghometemperature

@app.route('/play')
def testplayer():
    return render_template('play.html')

@app.route('/play', methods=["POST"])
def gamePlayerSetQuery():
    devices = ghomedevice.Device.objects
    data = '['
    for device in devices :
        data+='{'
        data+='"type" : '+'"'+str(device.__class__.__name__)+'"'+','
        data+='"ident" : '+'"'+str(device.physic_id)+'"'+','
        data+='"state" : '+'"'+str(device.current_state)+'"'+','
        data+='"coordX" : '+'"'+str(device.coordX)+'"'+','
        data+='"coordY" : '+'"'+str(device.coordY)+'"'
        data+='},'
    data = data[:len(data)-1]
    data +=']'
    return json.dumps(data)

@app.route('/play/location', methods=["POST"])
def getPosition():
    ident = request.form["ident"]
    absc = request.form['abscissa'] #min = 35 max = 610
    ordo = request.form['ordinate'] #min = 40 max = 545

    #### TEST ##A REMPLACER PAR UN ENVOI DE TRAME#####
    upDev = ghomedevice.Device.objects(physic_id=ident)[0]
    upDev.coordX = absc
    upDev.coordY = ordo
    upDev.save()
    ##################################################

    return render_template('play.html')
	
@app.route('/play/captor', methods=["POST"])
def getCaptor():
    idCaptor = request.form['captor']
    
    #### TEST ##A REMPLACER PAR UN ENVOI DE TRAME#####
    ghomedevice.Device.objects(physic_id=idCaptor)[0].update("open")
    ##################################################

    return render_template('play.html')

