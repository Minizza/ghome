#!/usr/bin/env python
# -*- coding: utf-8 -*-

import loggerConfig

## on récupère la configuration par défaut : afficher les message Warning et de
#  priorité supérieur dans la console et dans le fichier de log
logger = loggerConfig.configure()

# apparraitra comme une ligne info dans le log
logger.info('Hello')
# apparraitra comme une ligne warning dans le log dans le log
logger.warning('Testing %s', 'foo')