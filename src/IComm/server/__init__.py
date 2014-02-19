#!/usr/bin/env python
# -*-coding:Utf-8 -*

from flask import Flask, render_template

import json
import sys

app = Flask(__name__)

import server.routes.connection
import server.routes.devices
import server.routes.draw
import server.routes.game
import server.routes.play
import server.routes.utilities

# Set secret key for session
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Index
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Config Object
try:
    with open('server/config.json', 'r') as fileconf:
        CONFIG = json.loads(fileconf.read())
except IOError:
    print "Can't load the configuration file. Exiting..."
    sys.exit()