#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : School.py
author: chris rogers
why   : base class for School db object
        it's a sql alchemy ORM thing
        it's intended to be a code representation of a School
        and able to marshaled and unmarshaled in/out of json
"""

# python modules

# 3rd party modules
from geoalchemy2 import Geometry
from sqlalchemy import (
        Column,
        Float,
        ForeignKey,
        Integer,
        String,
)
from sqlalchemy.dialects import postgresql

# gearmap modules
from db_models.base import Base
from GearmapConfig import GearmapConfig

DB_CFG = GearmapConfig()


class School(Base):
    """SQL Alchemy class for a School object."""
    __tablename__ = DB_CFG.DEV_DBCONFIG.school_table

    id = Column('id', Integer, primary_key=True)
    school = Column('school', String)
    canonical_name = Column('canonical_name', String)
    abbreviation = Column('abbreviation', String)
    nicknames = Column('nicknames', postgresql.ARRAY(postgresql.TEXT))
    city = Column('city', String)
    state = Column('state', String)
    conference = Column('conference', String)
    conference_id = Column(
        'conference_id',
        Integer,
        ForeignKey(
            DB_CFG.DEV_DBCONFIG.conference_table + '.id',
            ondelete='CASCADE'
            ),
        nullable=False
    )
    latitude = Column('latitude', Float)
    longitude = Column('longitude', Float)
    population = Column('population', Integer)
    stadium_capacity = Column('stadium_capacity', Integer)
    school_geometry = Column('school_geometry', Geometry('POINT'))
    marker = Column('marker', String)

    def create(self,
               school,
               canonical_name,
               abbreviation,
               nicknames,
               city,
               state,
               conference,
               conference_id,
               latitude,
               longitude,
               population,
               stadium_capacity,
               marker,
               school_geometry=None):
        """Create a School object."""
        self.school = school
        self.nicknames = nicknames
        self.canonical_name = canonical_name
        self.abbreviation = abbreviation
        self.city = city
        self.state = state
        self.conference = conference
        self.conference_id = conference_id
        self.latitude = latitude
        self.longitude = longitude
        self.population = population
        self.stadium_capacity = stadium_capacity
        self.marker = marker
        self.school_geometry = school_geometry

    @classmethod
    def from_json(cls, data):
        """Construct a School obj from a json blob."""
        return cls(**data)

    def to_json(self):
        """Convert a School obj to a json blob."""
        attr_names = [
                'id',
                'school',
                'canonical_name',
                'abbreviation',
                'nicknames',
                'city',
                'state',
                'conference',
                'conference_id',
                'latitude',
                'longitude',
                'marker',
                'population',
                'stadium_capacity',
                'school_geometry',
                ]

        attr_vals = [getattr(self, attr) for attr in attr_names]
        return dict(zip(attr_names, attr_vals))
