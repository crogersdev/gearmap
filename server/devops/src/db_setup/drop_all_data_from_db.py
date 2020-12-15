#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : drop_all_data_from_db.py
author: chris rogers
why   : run this script when you want to destroy all app related db entries
        e.g. schemas, tables, etc...
"""

# python modules
import asyncio
import sys

# 3rd party modules
from psycopg2 import Error as PgError

# gearmap modules
import destroy_db_sql_statements as sql_cmds
from GearmapConfig import GearmapConfig
from GearmapDbSession import GearmapDbSession

CFG = GearmapConfig()
db_session = GearmapDbSession()


async def destroy_them_all(db_session, quiet=False):
    """asynchronously drop all data in database."""

    env = db_session.which_env()

    try:
        await db_session.execute_raw_sql(sql_cmds.drop_observation_table(env))
        if not quiet:
            print("Destroyed %s table" % CFG.DEV_DBCONFIG.observation_table)

        await db_session.execute_raw_sql(sql_cmds.drop_conference_table(env))
        if not quiet:
            print("Destroyed %s table" % CFG.DEV_DBCONFIG.conference_table)

        await db_session.execute_raw_sql(sql_cmds.drop_school_table(env))
        if not quiet:
            print("Destroyed %s table" % CFG.DEV_DBCONFIG.school_table)

        await db_session.execute_raw_sql(sql_cmds.drop_gearmap_schema(env))
        if not quiet:
            print("Destroyed %s schema" % CFG.DEV_DBCONFIG.dbschema)

    except PgError as error:
        print("Errors destroying database:")
        print('\t' + str(error.pgerror))
        print('\tWARNING: It is possible the database was not fully destroyed'
              'and is now in an undefined state.  Please try to destroy again.')
        raise BaseException('Errors destroying database.')

if __name__ == '__main__':

    try:
        which_env = sys.argv[1]
    except IndexError:
        which_env = 'dev'

    if which_env != 'dev' and which_env != 'integration_test':
        print('please call me with either "dev" (default) or "integration_test"')
        sys.exit()

    session = GearmapDbSession(env=which_env)
    loop = asyncio.get_event_loop()
    task = loop.create_task(destroy_them_all(session))
    loop.run_until_complete(task)
    print("Done!")
