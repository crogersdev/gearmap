#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : DBConnectionError.py
author: chris rogers
why   : nice to have custom connection error messages.  i think this is
        still mostly a wip
"""

# python modules=

# 3rd party modules

# gearmap modules


class DbConnectionError(Exception):
    """ inherits from base exception
        TODO: make it inherit from a specific exception
    """
    def __init__(self, error_args):
        Exception.__init__(self, '{}'.format(error_args))
        self.error_args = error_args
