#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : put_conferences_in_db.py
author: chris rogers
why   : csv reader for wiki-scraped csv file that has 11 FBS conferences
"""


# python modules
import asyncio
from csv import DictReader
import sys

# 3rd party modules
from shapely.geometry import Point, Polygon

# gearmap modules
from db_models.Conference import Conference
from GearmapConfig import GearmapConfig
from GearmapDbSession import GearmapDbSession


CFG = GearmapConfig()


async def add_conferences(
        session,
        quiet=False
        ):
    """Add conferences asynchronously"""
    # TRICKY: Path to cfb_conferences.csv is relative to who calls it.
    # TODO(me): make this a configurable path or something less brittle
    with open('/gearmap/devops/src/db_setup/cfb_conferences.csv', 'r', newline='\n') as confs_file:
        READER = DictReader(confs_file)
        for count, row in enumerate(READER):
            if count == 0:
                continue

            row['geometry'] = None

            row['marker'] = row['name'].lower().replace(' ', '_') + '_marker'

            # TRICKY: from_json is a classmethod, which is 
            #         a kooky alternate way of doing a ctor
            try:
                await session.add(Conference.from_json(row))
            except TypeError:
                print('You had an error in your CSV row.  Skipping...')
                print(row)

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
    task = loop.create_task(add_conferences(session))
    loop.run_until_complete(task)
    print("Done putting conferences in database!")
