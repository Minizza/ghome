#!/usr/bin/env python
# -*-coding:Utf-8 -*

from server import app
from server import CONFIG


def main():
	app.run(host=CONFIG['host'], debug=CONFIG['debug'], port=CONFIG['port'])	

#app.run(host='0.0.0.0')
if __name__ == '__main__':
	main()
