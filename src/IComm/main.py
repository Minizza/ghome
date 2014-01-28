#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from mongoengine import *
import Model.Place.ghomeuser as ghomeuser
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    monTexte = "Ceci est la page d'accueil du site"
    return render_template('index.html', data=monTexte)
	
@app.route('/connection')
def connection():
    return render_template('connection.html')
	

@app.route('/connection',  methods=["POST"])
def connection_post():
	username = request.form['username']
	password = request.form['password']
	
	connect('test')
	for user in ghomeuser.GHomeUser.objects:
		if user.name == username:
			if user.password == password:
				find = 1
		else:
			find = 0
	
	if find:
		return render_template('index.html')
	else : 
		return render_template('connection.html')
			

@app.route('/devices')
def devices():
    devices = 0 # Fetch les devices depuis la BD ici !
    return render_template('devices.html', devices=devices)

if __name__ == '__main__':
    app.run(debug=True)