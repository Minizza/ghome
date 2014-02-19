#!/usr/bin/env python
# -*-coding:Utf-8 -*

from functools import wraps
from flask import session, redirect
from server.routes.utilities import *

# Decorator to check roles
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                return error("Eh oh tu t'as pas les droits la","page inaccessible")
            return f(*args, **kwargs)
        return wrapped
    return wrapper

# Authentication
def get_current_user_role():
    if 'role' in session:
        return session['role']
    return None

def set_current_user_role(role):
    session['role'] = role