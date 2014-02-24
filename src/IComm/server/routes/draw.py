#!/usr/bin/env python
# -*-coding:Utf-8 -*

from server import app, CONFIG
from flask import render_template, request
from server.roles import *

@app.route('/draw')
def draw():
    return render_template('draw.html')

@app.route('/draw', methods=["POST"])
def save_svg():
    if "svg" in request.form:
        with open('../src/IComm/server/{}.svg'.format(CONFIG['nom_plan']), 'w') as fichiersvg:
            fichiersvg.write(request.form['svg'])
    return "OK"

