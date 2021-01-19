#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : app.py
author: chris rogers
why   : starts the app
"""

# python modules
import asyncio

# 3rd party modules
from aiohttp import web

# gearmap modules
from api.api_v1 import create_gearmap_app
from api.GearmapImpl import GearmapImpl
from GearmapConfig import GearmapConfig
from utils.logger import logger


logger.name = __name__
WEBAPP_CFG = GearmapConfig()

app = create_gearmap_app(loop=asyncio.get_event_loop())
app['GearmapImpl'] = GearmapImpl()
print('finny')
logger.debug("Running web app")
web.run_app(app, port=WEBAPP_CFG.DEV_WEBAPPCONFIG.port)
