#!/usr/bin/env python
# -*-coding:Utf-8 -*

from server import app
from flask import render_template, request, session
from server.roles import *
from mongoengine import *
import Model.Place.ghomeuser as ghomeuser

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
        return render_template('connection.html', notif_title="Wrong login or password", notif_content="Please try again.", notif_type="danger")

@app.route('/logout')
def logout():
    session.pop('role', None)
    return connection()

