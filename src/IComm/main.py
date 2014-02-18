#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from functools import wraps
from flask import Flask, render_template, request, session, redirect
from mongoengine import *

import json

import Model.Place.ghomeuser as ghomeuser

import Model.Device.device as ghomedevice
import Model.Device.sensor as ghomesensor
import Model.Device.actuator as ghomeactuator
import Model.Device.temperature as ghometemperature
import Model.Device.DeviceFactory as factories

import tests.base as testdata

import forms.NewDeviceForm as forms

from flask import Flask, render_template, request

app = Flask(__name__)

# Set secret key for session
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Decorator to check roles
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                return error("Eh oh tu t'as pas les droits là","page inaccessible")
            return f(*args, **kwargs)
        return wrapped
    return wrapper

# Authentication
def get_current_user_role():
    if 'role' in session:
        return session['role']
    return None

def set_current_user_role(role):
    session['role'] = role

# Routes

@app.route('/')
def index():
    monTexte = "Ceci est la page d'accueil du super site"
    return render_template('index.html', data=monTexte, notif_title="Titre", notif_content="je suis sur l'index", notif_type="success")
    
@app.route('/connection')
def connection():
    return render_template('connection.html')
	
@app.route('/testtemp')
def testTemperature():
    connect('test')
    devices = ghometemperature.Temperature.objects
    return render_template('testtemp.html', devices=devices)

@app.route('/testplayer')
def testplayer():
    return render_template('testplayer.html')
	
@app.route('/testplayer', methods=["POST"])
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
	
@app.route('/testplayer/location', methods=["POST"])
def getPosition():
	ab = request.form['abscissa']
	ord = request.form['ordinate']
	print ab
	print ord
	return render_template('testplayer.html')
    

@app.route('/connection', methods=["POST"])
def connection_post():
    username = request.form['username']
    password = request.form['password']
    
    connect('test')
    find = 0
    for user in ghomeuser.GHomeUser.objects:
        if user.name == username:
            if user.password == password:
                find = 1
                session['role'] = user.role
    
    if find:
        return render_template('index.html')
    else : 
        return render_template('connection.html', notif_title="Wrong login or password", notif_content="Please try again.", notif_type="danger")

def fetchDevices():
    devices = ghomedevice.Device.objects # Fetch les devices depuis la BD ici !
    for device in devices:
        device.type = type(device).__name__
    return devices

@app.route('/devices', methods=["GET", "POST"])
@requires_roles('admin')
def devices():
    connect('test')
    newForm = forms.NewDeviceForm()
    if newForm.validate_on_submit():
        new = factories.DeviceFactory.newDevice(newForm.device_type.data, newForm.physic_id.data, newForm.name.data)
        try:
            new.save()
        except NotUniqueError as e:
            return render_template('devices.html', devices=fetchDevices(), form=newForm, notif_title="Unique constraint violation", notif_content=e, notif_type="danger")
        return redirect('/devices')
    else:
        return render_template('devices.html', devices=fetchDevices(), form=newForm)

@app.route('/devices/remove', methods=["POST"])
@requires_roles('admin')
def remove_device():
    connect('test')
    devicePhysicId = request.form['physic_id']
    device = ghomedevice.Device.objects(physic_id = devicePhysicId)
    #Vérification si objet existant ?
    device.delete()
    return redirect('/devices')


@app.route('/draw')
def draw():
    return render_template('draw.html')

@app.route('/draw', methods=["POST"])
def save_svg():
    if "svg" in request.form:
        with open('{}.svg'.format(CONFIG['nom_plan']), 'w') as fichiersvg:
            fichiersvg.write(request.form['svg'])
    return "OK"

@app.route('/logout')
def logout():
    session.pop('role', None)
    return connection()

@app.route('/error')
def error(content="Une erreur est survenue.", type="", head="Erreur"):
    return render_template('error.html', head=head, type=type, content=content)


@app.route('/launchGame')
def launchGame():
    return render_template('gameView.html')

@app.route('/launchGame', methods=["POST"])
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

# Config Object
CONFIG = json.loads(open('config.json').read())

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True, port=5000)

