#!/usr/bin/env python
# -*-coding:Utf-8 -*

from server import app, CONFIG
from flask import render_template, request
from server.roles import *
import json
from mongoengine import *
import Model.Device.device as ghomedevice
import Model.Device.temperature as ghometemperature
from Model.Device.position import Position

@app.route('/play')
def testplayer():
    players = Position.objects()
    return render_template('play.html', plan = CONFIG['nom_plan'], players = players)

@app.route('/play', methods=["POST"])
def gamePlayerSetQuery():
    devices = ghomedevice.Device.objects
    data = '['
    for device in devices :
        data+='{'
        data+='"type" : '+'"'+str(device.__class__.__name__)+'"'+','
        data+='"ident" : '+'"'+str(device.physic_id)+'"'+','
        if ("Position" in str(device.__class__.__name__)) :
            data+='"state" : {'+'"coordX" : "'+str(device.current_state.get('coordX'))+'", "coordY" : "'+str(device.current_state.get('coordY'))+'"},'
            data+='"team" : '+'"'+str(device.team)+'"'+','
        else :
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
    absc = request.form["abscissa"] #min = 35 max = 610
    ordo = request.form["ordinate"] #min = 40 max = 545

    #### TEST ##A REMPLACER PAR UN ENVOI DE TRAME#####
    upDev = ghomedevice.Device.objects(physic_id=ident)[0]
    upDev.moving(int(absc),int(ordo))
    ##################################################
    return "ok"

	
@app.route('/play/captor', methods=["POST"])
def sendActivCaptor():
    idCaptor = request.form['captor']
    #### TEST ##A REMPLACER PAR UN ENVOI DE TRAME#####
    ghomedevice.Device.objects(physic_id=idCaptor)[0].update("open")
    ##################################################
    return "ok"

@app.route('/play/nocaptor', methods=["POST"])
def sendNoActivCapt():
    idCaptor = request.form['captor']
    #### TEST ##A REMPLACER PAR UN ENVOI DE TRAME#####
    ghomedevice.Device.objects(physic_id=idCaptor)[0].update("close")
    ##################################################
    return "ok"

