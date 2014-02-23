#!/usr/bin/env python
# -*-coding:Utf-8 -*

from flask import Flask, render_template
from logger import LOGGER

import os

import json
import sys

def get_real_path(path):
	root = os.path.dirname(__file__)
	path = os.path.abspath(os.path.join(root, path))
	return path

app = Flask(__name__)

# Config Object
try:
    with open(get_real_path('config.json'), 'r') as fileconf:
        CONFIG = json.loads(fileconf.read())
except IOError:
    LOGGER.error("Can't load the configuration file. Exiting...")
    sys.exit()

import server.routes.connection
import server.routes.devices
import server.routes.draw
import server.routes.game
import server.routes.play
import server.routes.utilities

# Set secret key for session
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Index
@app.route(get_real_path('/'))
@app.route(get_real_path('/index'))
def index():
    return render_template('index.html')
