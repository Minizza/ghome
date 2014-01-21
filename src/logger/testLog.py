#!/usr/bin/env python
# -*- coding: utf-8 -*-

import loggerConfig

logger = loggerConfig.configure(loggerConfig.logging.WARN)
# Après 3 heures, on peut enfin logguer
# Il est temps de spammer votre code avec des logs partout :
logger.info('Hello')
logger.warning('Testing %s', 'foo')