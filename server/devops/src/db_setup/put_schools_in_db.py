#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : put_schools_in_db.py
author: chris rogers
why   : csv reader for wiki-scraped csv file that has all 120 FBS teams
"""


# python modules
import asyncio
from csv import DictReader
import sys

# 3rd party modules
from shapely.geometry import Point
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

# gearmap modules
from db_models.Conference import Conference
from db_models.School import School
from GearmapConfig import GearmapConfig
from GearmapDbSession import GearmapDbSession
from utils import logger


CFG = GearmapConfig()


async def add_schools(
        session,
        quiet=False
        ):
    """Add schools asynchronously"""
    # TRICKY: Path to cfb_teams.csv is relative to who calls it.
    # TODO(me): make this a configurable path or something less brittle
    with open('/gearmap/devops/src/db_setup/cfb_teams.csv', 'r', newline='\n') as teams_file:
        READER = DictReader(teams_file)
        for count, row in enumerate(READER):
            if count == 0:
                continue

            if not quiet:
                print("Creating school geometry for %s at location (%s, %s)" %
                      (row['school'], row['longitude'], row['latitude']))

            row['school_geometry'] = Point(
                float(row['longitude']),
                float(row['latitude'])
            ).wkt

            csv_conf_abbrev = row['conference']
            conf_search_pattern = "%{}%".format(csv_conf_abbrev)
            conf_search_pattern = conf_search_pattern.replace(' ', '%')

            conf_q = await session.query(
                Conference
            )

            try:
                conference = conf_q.filter(
                    or_(
                        Conference.abbrev.ilike(conf_search_pattern),
                        Conference.name.ilike(conf_search_pattern)
                    )
                ).all()
                conference = conference[0]
            except NoResultFound:
                print("Unable to find conference upon adding a school")
                raise

            row['conference_id'] = conference.id

            if row['stadium_capacity'] == 'None':
                row['stadium_capacity'] = -1

            row['marker'] = row['school'].lower().replace(' ', '_') + '_marker'

            # TRICKY: from_json is a classmethod, which is 
            #         a kooky alternate way of doing a ctor
            await session.add(School.from_json(row))

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
    task = loop.create_task(add_schools(session, True))
    loop.run_until_complete(task)
    logger.info("Done putting schools in database!")
