#!/usr/bin/env python
# -*-coding:Utf-8 -*

from server import app
from flask import render_template
from server.roles import *
import json
import Model.Device.device as ghomedevice

@app.route('/game')
def launchGame():
    return render_template('game.html')


@app.route('/game', methods=["POST"])
def gameSetQuery():
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

