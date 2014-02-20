#!/usr/bin/env python
# -*-coding:Utf-8 -*

from server import app
from server import CONFIG


#app.run(host='0.0.0.0')
app.run(host=CONFIG['host'], debug=CONFIG['debug'], port=CONFIG['port'])