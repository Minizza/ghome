#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from functools import wraps
from flask import Flask, render_template, request, session
from mongoengine import *

import Model.Place.ghomeuser as ghomeuser

import Model.Device.device as ghomedevice
import Model.Device.sensor as ghomesensor
import Model.Device.actuator as ghomeactuator
import tests.base as testdata

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
                return error('privileges')
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
    monTexte = "Ceci est la page d'accueil du site"
    return render_template('index.html', data=monTexte)
    
@app.route('/connection')
def connection():
    return render_template('connection.html')
    

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
        return render_template('connection.html')

@app.route('/devices', methods=["POST"])
@requires_roles('admin')
def add_device():
    connect('test')
    new = ghomesensor.Sensor(physic_id="ihfd", name="toto")
    new.save()
    return devices()

@app.route('/devices')
@requires_roles('admin')
def devices():
    connect('test')
    devices = ghomedevice.Device.objects # Fetch les devices depuis la BD ici !
    return render_template('devices.html', devices=devices)

@app.route('/logout')
def logout():
    session.pop('role', None)
    return connection()

@app.route('/error/<type>')
def error(type):
    if type == 'privileges':
        return render_template('error_privileges.html')
    return index()

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True, port=5000)

