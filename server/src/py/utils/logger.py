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

# TODO: fix...  this will fail if the folder /gearmap/logs doesn't exist, and it doesn't by default.  the code doesn't create it.
logging.basicConfig(
  filename="/gearmap/logs/" + APP_CFG.DEV_APPCONFIG.app_log_filename,
  level=logging.DEBUG
)

root = logging.getLogger(name=APP_CFG.DEV_APPCONFIG.app_logger_name)
root.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(sys.stdout)
stderr_handler = logging.StreamHandler(sys.stderr)
stdout_handler.setLevel(logging.DEBUG)
stderr_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)
stderr_handler.setFormatter(formatter)

# HACK: i don't know why, but a new handler is added every time
#       this module is invoked... so i'm going to patch that with this if
#       statement
if not root.handlers:
    root.addHandler(stdout_handler)
    root.addHandler(stderr_handler)

# the object to be imported
logger = root
