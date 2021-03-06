#!/usr/bin/env python
# -*-coding:Utf-8 -*

from server import app, CONFIG
from flask import render_template, request, redirect
from server.roles import *
from mongoengine import *
import Model.Device.device as ghomedevice
import Model.Device.DeviceFactory as factories
import server.forms.NewDeviceForm as forms
import json

import server.controller as controller

def loadPlan():
    try:
        with open("../src/IComm/server/"+CONFIG['nom_plan']+".svg") as ficPlan:
            return ficPlan.read()
    except IOError as e:
        return None
    return None

@app.route('/devices', methods=["GET", "POST"])
@requires_roles('admin')
def devices():
    connect('test')
    newForm = forms.NewDeviceForm()
    plan = loadPlan()
    if newForm.validate_on_submit():
        new = factories.DeviceFactory.newDevice(newForm.device_type.data, newForm.physic_id.data, newForm.name.data)
        try:
            new.save()
        except NotUniqueError as e:
            return render_template('devices.html', devices=controller.fetchDevices(), plan=plan, form=newForm, notif_title="Unique constraint violation", notif_content=e, notif_type="danger")
        return redirect('/devices')
    else:
        return render_template('devices.html', devices=controller.fetchDevices(), plan=plan, form=newForm)

@app.route('/devices/remove', methods=["POST"])
@requires_roles('admin')
def remove_device():
    connect('test')
    devicePhysicId = request.form['physic_id']
    device = ghomedevice.Device.objects(physic_id = devicePhysicId)
    #Vérification si objet existant ?
    device.delete()
    return redirect('/devices')

@app.route('/devices/addDeviceToPlan', methods=["POST"])
@requires_roles('admin')
def add_device_to_plan():
    physic_id = request.form["physic_id"]
    x = request.form["x"]
    y = request.form["y"]
    print x
    devicePlace = ghomedevice.Device.objects(physic_id=physic_id)[0]
    devicePlace.coordX = x
    devicePlace.coordY = y
    devicePlace.save()
    devices = ghomedevice.Device.objects
    data='{'
    data+='"physic_id" : '+'"'+devicePlace.physic_id+'"'+','
    data+='"x" : '+'"'+str(devicePlace.coordX)+'"'+','
    data+='"y" : '+'"'+str(devicePlace.coordY)+'"'
    data+='}'
    return json.dumps(data)
