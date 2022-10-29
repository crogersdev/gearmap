#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : logger.py
author: chris rogers
why   : move all python logger boilerplate to one location
"""

import logging
import sys

from GearmapConfig import GearmapConfig

APP_CFG = GearmapConfig()
cfg = APP_CFG.DEV_APPCONFIG

# TODO: fix...  this will fail if the folder /gearmap/logs doesn't exist, and it doesn't by default.  the code doesn't create it.
log_file = cfg.app_logger_path + '/' + cfg.app_log_filename

logFormatter = logging.Formatter("%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("{0}/{1}".format(cfg.app_logger_path, cfg.app_log_filename))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

rootLogger.setLevel(logging.DEBUG)

logger = rootLogger
