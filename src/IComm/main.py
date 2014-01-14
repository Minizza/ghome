#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    monTexte = 'Hello World'
    return render_template('index.html', helloworld=monTexte)

if __name__ == '__main__':
    app.run(debug=True)