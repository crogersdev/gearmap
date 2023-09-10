#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : GearmapDbBase.py
author: chris rogers
why   : base class for sql alchemy ORM database classes
        it's my intention to inherit from this class for each  -- dev, test,
        qa, prod, etc...  but we'll see how that turns out.

        we'll use this base class to create a db engine in sql alchemy
        which doesn't actually connect to the database, but abstracts the
        connection details
"""

# python modules
import asyncio
import sys

# 3rd party modules
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import (
    create_database,
    database_exists,
)
from sqlalchemy.orm import relationship

# gearmap modules
from db_models.base import Base
from db_models.Observation import Observation
from db_models.Conference import Conference
from db_models.School import School
from GearmapConfig import GearmapConfig
from GearmapDbSession import GearmapDbSession
from utils.logger import logger

DB_CFG = GearmapConfig()


async def create_all(db_session, quiet=False):
    """Create all db's."""

    e = db_session.get_engine()
    if not database_exists(e.url):
        logger.debug(f"attempting to create a database: {e.url}")
        create_database(e.url)

    try:
        try:
            resp = await db_session.execute_raw_sql('SELECT PostGIS_full_version();')
            resp_list = resp.fetchall()
        except ProgrammingError:
            resp_list = []
            pass  # TRICKY: if we fail to get Postgis, then just create it.
        except BaseException as be:
            if "PostGIS_full_version()" in str(be):
                resp_list = []
                pass
            else:
                raise be

        if not any([True if 'POSTGIS=' in str(x) else False for x in resp_list]):
            if not quiet:
                logger.debug("Creating postgis extensions for the Gearmap DB...")
            db_session.create_postgis_extension()
            if not quiet:
                logger.debug("Done!")

        if not quiet:
            logger.debug(f"SQL Alchemy is creating DB objects for the {db_session.which_env()} Gearmap DB...")

        School.conference_affiliation = relationship("Conference")
        School.observations = relationship("Observation")

        Base.metadata.create_all(db_session.get_engine())

        if not quiet:
            logger.debug(f"SQL Alchemy is done creating DB objects for the {db_session.which_env()} Gearmap DB!")

    except Exception as e:
        raise BaseException("Unable to create_all in SQL Alchemy:", str(e))


if __name__ == '__main__':

    try:
        which_env = sys.argv[1]
    except IndexError:
        which_env = 'dev'

    if which_env != 'dev' and which_env != 'integration_test':
        logger.debug('please call me with either "dev" (default) or "integration_test"')
        sys.exit()

    db_session = GearmapDbSession(env=which_env)
    loop = asyncio.get_event_loop()
    task = loop.create_task(create_all(db_session))
    loop.run_until_complete(task)
    logger.debug("Done!")
