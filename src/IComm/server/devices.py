#!/usr/bin/env python
# -*-coding:Utf-8 -*

from server import app
from flask import render_template, request, redirect
from server.roles import *
from mongoengine import *
import Model.Device.device as ghomedevice
import Model.Device.DeviceFactory as factories
import forms.NewDeviceForm as forms

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