#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : base.py
author: chris rogers
why   : we need a sqlalchemy declarative_base object to use sqlalchemy to create
        all our tables.  it makes the most sense to put it here, alone, where
        the file can then be imported elsewhere its needed, rather than in a larger
        file/module/library that might also import something that needs it, which
        would create a circular dependency
"""

# python modules

# 3rd party modules
from sqlalchemy.ext.declarative import declarative_base

# gearmap modules


Base = declarative_base()
