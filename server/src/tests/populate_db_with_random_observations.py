#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : populate_db_with_random_observations.py
author: chris rogers
why   : puts data in the observations table so we have some fake data
        to work with.
"""

# python modules
import asyncio
from random import choice
from random import seed
from random import uniform
import sys
import time

# 3rd party modules
from sqlalchemy import func

# gearmap modules
from db_models.School import School
from db_models.Observation import Observation
from GearmapDbSession import GearmapDbSession

# http://en.wikipedia.org/wiki/Extreme_points_of_the_United_States#Westernmost
TOP = 49.3457868      # north lat
LEFT = -124.7844079   # west long
RIGHT = -66.9513812   # east long
BOTTOM = 24.7433195   # south lat

seed(time.process_time())


async def insert_fake_observations(
        session,
        num_fake_observations=5000,
        quiet=False
        ):
    """Insert a fake observation record.
       Meant to be used with integration testing.
    """

    async def create_fake_observation():
        lat = uniform(BOTTOM, TOP)
        lng = uniform(LEFT, RIGHT)

        which_school = choice(range(0, 4))

        if which_school == 0:
            s = 'Utah State'
        elif which_school == 1:
            s = 'Virginia Tech'
        elif which_school == 2:
            s = 'Rutgers'
        else:
            s = 'Virginia'

        school_coroutine = await session.query(School)
        filtered_schools = school_coroutine.filter(School.school == s)
        school = filtered_schools.all()[0]

        if not quiet:
            print("inserting %s seen at (lat: %02f, long: %02f)" % (s, lat, lng))

        observation_geom = func.ST_GeomFromText(
            'POINT({} {})'.format(lng, lat)
        )

        return Observation(
            school_id=school.id,
            observed_lat=lat,
            observed_long=lng,
            observation_geom=observation_geom
        )

    if not quiet:
        print("Inserting %s records into the observations data table"
              % num_fake_observations)

    chunk_size = 1000
    chunks = int(num_fake_observations / chunk_size)
    remainder = num_fake_observations % chunk_size

    for i in range(0, chunks):
        chunk_of_observations = []

        for j in range(0, chunk_size):

            chunk_of_observations.append(
                await create_fake_observation()
            )

        await session.bulk_insert(chunk_of_observations)
        chunk_of_observations = []

    if not remainder:
        chunk_of_observations = []
        for i in range(0, remainder):
            chunk_of_observations.append(
                await create_fake_observation()
            )
        await session.bulk_insert(chunk_of_observations)


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
    task = loop.create_task(insert_fake_observations(session, quiet=False))
    loop.run_until_complete(task)
    print("Done!")
