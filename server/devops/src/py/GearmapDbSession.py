#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : GearmapDbSession.py
author: chris rogers
why   : wrapper and getter for sql alchemy ORM db session
        iow, i don't want to keep typing the same nonsense over and over just
        to interact with the durn db
"""

# python modules
from functools import wraps
import os

# 3rd party modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# gearmap modules
from GearmapConfig import GearmapConfig
from utils.logger import logger

DB_CFG = GearmapConfig()


def fails_gracefully(func):
    """Ensure the called function handles exceptions properly."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """Call the wrapped function."""
        try:
            ret_val = func(self, *args, **kwargs)
        except ValueError as e:
            raise Exception(f'Required value provided was not the correct type; details: {e}')
        except Exception as e:
            raise Exception(f'Problem found in {__file__}: {e}')
        return ret_val
    return wrapper


class GearmapDbSession(object):
    """Wraps and handles SQL Alchemy sessions and the like."""

    @fails_gracefully
    def __init__(self, env="dev"):
        """Create a db engine and set all public vars."""

        self._logger = logger
        self._db_env = env

        if not isinstance(self._db_env, str):
            raise Exception(
                'Intended environment provided for DB setup was not a string. ' +
                'Provided environment: %s' % (self._db_env)
            )

        if 'dev' in str(self._db_env).lower():
            dbuser = DB_CFG.DEV_DBCONFIG.dbuser
            dbpasswd = DB_CFG.DEV_DBCONFIG.dbpasswd
            dbhost = DB_CFG.DEV_DBCONFIG.dbhost
            dbport = DB_CFG.DEV_DBCONFIG.dbport
            dbname = DB_CFG.DEV_DBCONFIG.dbname
        elif 'integration_test' in str(self._db_env).lower():
            dbuser = DB_CFG.INTEGRATION_TEST_DBCONFIG.dbuser
            dbpasswd = DB_CFG.INTEGRATION_TEST_DBCONFIG.dbpasswd
            dbhost = DB_CFG.INTEGRATION_TEST_DBCONFIG.dbhost
            dbport = DB_CFG.INTEGRATION_TEST_DBCONFIG.dbport
            dbname = DB_CFG.INTEGRATION_TEST_DBCONFIG.dbname
        else:
            raise Exception(
                'Unable to determine proper operating environment for DB. ' +
                'Provided environment: %s' % (self._db_env)
            )

        self._engine_str = 'postgresql://%s:%s@%s:%s/%s' % (
            dbuser, dbpasswd, dbhost, dbport, dbname
        )
        self._db_engine = create_engine(self._engine_str)
        self._session_creator = sessionmaker(bind=self._db_engine)
        self._session = self._session_creator()

    def which_env(self):
        return str(self._db_env).lower()

    def rollback(self):
        """ call rollback in sqlalchemy """
        self._session.rollback()

    @fails_gracefully
    def __del__(self):
        """ destructor; close the session """
        self._session.close()

    @fails_gracefully
    async def add(self, thing):
        """Add something."""
        self._session.add(thing)
        self._session.commit()

    @fails_gracefully
    async def delete(self, thing):
        """Delete something."""
        self._session.delete(thing)
        self._session.commit()

    @fails_gracefully
    async def query(self, *args, **kw):
        """Query the db."""
        return self._session.query(*args, **kw)

    @fails_gracefully
    async def execute_raw_sql(self, sql):
        """Execute raw sql.  this is a terrible idea."""
        if self._session:
            self._session.commit()

        with self._db_engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT")
            result_set = conn.execute(sql)

        return result_set

    @fails_gracefully
    async def get_session(self):
        """Return the session object."""
        return self._session

    @fails_gracefully
    def get_engine(self):
        """Return the db engine."""
        # TODO(me): is this a good idea?
        return self._db_engine

    @fails_gracefully
    def get_engine_url(self):
        """Return the engine URL."""
        return self._db_engine.url

    @fails_gracefully
    def create_postgis_extension(self):
        """Create postgis extension for the db engine."""
        with self._db_engine.connect() as conn:
            conn.execute('CREATE EXTENSION postgis CASCADE;')
            conn.execute('CREATE EXTENSION postgis_topology CASCADE;')

    @fails_gracefully
    async def bulk_insert(self, objects):
        """Perform bulk insert.
           requires the objects param to be a list
        """
        if not isinstance(objects, list):
            raise ValueError('bulk_insert() requires a list of objects')
        self._session.add_all(objects)
        self._session.commit()
