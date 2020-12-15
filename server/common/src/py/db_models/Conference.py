#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : Conference.py
author: chris rogers
why   : base class for Conference db object
        it's a sql alchemy ORM thing
        it's intended to be a code representation of a Conference,
        and able to marshaled and unmarshaled in/out of json
"""

# python modules

# 3rd party modules
from geoalchemy2 import Geometry
from sqlalchemy import (
        Column,
        Integer,
        String,
)

# gearmap modules
from db_models.base import Base
from GearmapConfig import GearmapConfig

DB_CFG = GearmapConfig()


class Conference(Base):
    """SQL Alchemy class for a School object"""

    __tablename__ = DB_CFG.DEV_DBCONFIG.conference_table

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    nickname = Column('nickname', String)
    abbrev = Column('abbrev', String)
    year_founded = Column('year_founded', Integer)
    num_members = Column('num_members', Integer)
    hq_city = Column('hq_city', String)
    hq_state = Column('hq_state', String)
    geometry = Column('geometry', Geometry('MULTIPOLYGON'))
    marker = Column('marker', String)

    def create(self,
               name,
               nickname,
               abbrev,
               year_founded,
               num_members,
               hq_city,
               hq_state,
               marker,
               geometry=None):
        """Create a conference object."""
        self.name = name
        self.nickname = nickname
        self.abbrev = abbrev
        self.year_founded = year_founded
        self.num_members = num_members
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.marker = marker
        self.geometry = geometry

    @classmethod
    def from_json(cls, data):
        """Construct a Conference object from a json blob."""
        return cls(**data)

    def to_json(self):
        """Convert a Conference obj to a json blob."""
        attr_names = [
                'id',
                'name',
                'nickname',
                'abbrev',
                'year_founded',
                'num_members',
                'hq_city',
                'hq_state',
                'geometry',
                'marker'
                ]

        attr_vals = [getattr(self, attr) for attr in attr_names]
        return dict(zip(attr_names, attr_vals))
