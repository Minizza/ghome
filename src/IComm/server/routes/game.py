#!/usr/bin/env python
# -*-coding:Utf-8 -*

from server import app, CONFIG
from flask import render_template, request
from server.roles import *
import json
import Model.Device.device as ghomedevice
from Model.update import lazzyUpdate
from logger import LOGGER

wichGame = []

@app.route('/game0')
def theGame0():
    return render_template('game.html', theGame = 0, plan = CONFIG['nom_plan'])
@app.route('/game1')
def theGame1():
    return render_template('game.html', theGame = 1, plan = CONFIG['nom_plan'])
@app.route('/game2')
def theGame2():
    return render_template('game.html', theGame = 2, plan = CONFIG['nom_plan'])


@app.route('/game', methods=["POST"])
def gameSetQuery():
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

@app.route('/game/activated', methods=["POST"])
def actiActiv():
    theIdent = request.form["ident"]
    LOGGER.info(theIdent)
    lazzyUpdate().sendTrame(theIdent,"toggle")
    return "ok"

