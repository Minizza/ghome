#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    monTexte = 'Hello World'
    return render_template('index.html', helloworld=monTexte)
	
@app.route('/connection')
def connection():
    monTexte = 'Connection'
    return render_template('connection.html', helloworld=monTexte)

@app.route('/devices')
def devices():
    devices = 0 # Fetch les devices depuis la BD ici !
    return render_template('devices.html', devices=devices)

if __name__ == '__main__':
    app.run(debug=True)