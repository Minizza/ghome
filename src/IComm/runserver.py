#!/usr/bin/env python
# -*-coding:Utf-8 -*
import sys
from server import app
from server import CONFIG


def main():
    try:
        app.run(host=CONFIG['host'], debug=CONFIG['debug'], port=CONFIG['port'])
    except KeyboardInterrupt:
        sys.exit(0)

#app.run(host='0.0.0.0')
if __name__ == '__main__':
    main()
