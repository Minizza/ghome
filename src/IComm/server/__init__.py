#!/usr/bin/env python
# -*-coding:Utf-8 -*

from flask import Flask, render_template

import json
import sys

app = Flask(__name__)

import server.connection
import server.devices
import server.draw
import server.game
import server.play

# Set secret key for session
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Index
@app.route('/')
def index():
    return render_template('index.html')

# Error
@app.route('/error')
def error(content="Une erreur est survenue.", type="", head="Erreur"):
    return render_template('error.html', head=head, type=type, content=content)

# Display temperatures
@app.route('/testtemp')
def testTemperature():
    connect('test')
    devices = ghometemperature.Temperature.objects
    return render_template('testtemp.html', devices=devices)

# Config Object
try:
    with open('server/config.json', 'r') as fileconf:
        CONFIG = json.loads(fileconf.read())
except IOError:
    print "Can't load the configuration file. Exiting..."
    sys.exit()
