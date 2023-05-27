#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : ResponseObject.py
author: chris rogers
why   : to have a defined format and schema for returned objects
        from the back end
"""

# python modules

# 3rd party modules

# gearmap modules


class GearmapResponse(object):
    """
    Return a GearmapResponse from the back end to the front end.

    Always.

    Status needs to be "success" or "fail".  Required.
    Message communicates the details of the status.  Not Required.
    Data is just whatever it is you want to send.  Required.

    """

    def __init__(self, status, data=None, message=None):
        self.status = status
        self.data = data if data else dict()
        self.message = message

    @classmethod
    def from_json(cls, data):
        """Construct a GearmapResponse object from a json blob."""
        return cls(**data)

    def to_json(self):
        """Convert a GearmapResponse object to json"""

        attr_names = [
            'status',
            'data',
            'message'
        ]

        attr_vals = [getattr(self, attr) for attr in attr_names]
        return dict(zip(attr_names, attr_vals))

    def to_string(self):
        """
        fill me in
        """

        return str(self.to_json())