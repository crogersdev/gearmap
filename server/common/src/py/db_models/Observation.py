#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : Observation.py
author: chris rogers
why   : base class for Observation db object
        it's a sql alchemy ORM thing
        it's intended to be a code representation of a Observation
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

# gearmap modules
from db_models.base import Base
from GearmapConfig import GearmapConfig

DB_CFG = GearmapConfig()


class Observation(Base):
    """SQL Alchemy class for an Observation object."""

    __tablename__ = DB_CFG.DEV_DBCONFIG.observation_table

    observation_id = Column('observation_id', Integer, primary_key=True)
    school_id = Column(
            'school_id',
            Integer,
            ForeignKey(
                DB_CFG.DEV_DBCONFIG.school_table + '.id',
                ondelete='CASCADE'
                ),
            nullable=False
            )
    gear_type = Column('gear_type', String)
    wearer_gender = Column('wearer_gender', String)
    wearer_ethnicity = Column('wearer_ethnicity', String)
    wearer_age = Column('wearer_age', Integer)
    observed_lat = Column('observed_lat', Float)
    observed_long = Column('observed_long', Float)
    observation_geom = Column('observation_geom', Geometry('POINT'))

    def create(self,
               observed_lat,
               observed_long,
               observation_geom,
               school_id,
               gear_type=None,
               wearer_gender=None,
               wearer_ethnicity=None,
               wearer_age=None):
        """Construct an Observation obj from values."""
        self.school_id = school_id
        self.gear_type = gear_type
        self.wearer_gender = wearer_gender
        self.wearer_ethnicity = wearer_ethnicity
        self.wearer_age = wearer_age
        self.observed_lat = observed_lat
        self.observed_long = observed_long
        self.observation_geom = observation_geom

        '''self.school_relationship = relationship(
            DB_CFG.DEV_DBCONFIG.school_table,
            back_populates=DB_CFG.DEV_DBCONFIG.observation_table
        )'''

    @classmethod
    def from_json(cls, data):
        """Construct an Observation obj from json blob."""
        return cls(**data)

    def to_json(self):
        """Convert an Observation object to json blob."""
        attr_names = [
                'school_id',
                'gear_type',
                'wearer_age'
                'wearer_gender',
                'wearer_ethnicity',
                'observed_lat',
                'observed_long',
                'observation_geom',
                ]

        attr_vals = [getattr(self, attr) for attr in attr_names]
        return dict(zip(attr_names, attr_vals))
