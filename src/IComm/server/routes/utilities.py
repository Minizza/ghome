#!/usr/bin/env python
# -*-coding:Utf-8 -*

from server import app
from flask import render_template

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