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

root = logging.getLogger(
    name=log_file
)
root.setLevel(logging.DEBUG)

output_file_handler = logging.FileHandler(log_file)
stdout_handler = logging.StreamHandler(sys.stdout)
stderr_handler = logging.StreamHandler(sys.stderr)
output_file_handler.setLevel(logging.DEBUG)
stdout_handler.setLevel(logging.DEBUG)
stderr_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
output_file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
stderr_handler.setFormatter(formatter)

# HACK: i don't know why, but a new handler is added every time
#       this module is invoked... so i'm going to patch that with this if
#       statement
if not root.handlers:
    root.addHandler(output_file_handler)
    root.addHandler(stdout_handler)
    root.addHandler(stderr_handler)

# the object to be imported
logger = root
