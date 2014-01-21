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
    return render_template('connection.html')
	
@app.route('/connection')
def manageConnection():
    return render_template('connection.html')

if __name__ == '__main__':
    app.run(debug=True)