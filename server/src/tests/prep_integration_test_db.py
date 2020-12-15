#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : prep_integration_test_db.py
author: chris rogers
why   : puts a canned set of data in the integration tests db.
        the point here is to make sure that integration tests
        run with the same data configuration; same observations,
        same everything
"""

# python modules
import asyncio

# 3rd party modules
from sqlalchemy import func

# gearmap modules
from canned_observation_positions_10k import locations

from test_utils import ball_state_school_id, usu_school_id

from GearmapDbBase import Observation
from GearmapDbSession import GearmapDbSession


async def insert_fake_observations(
        session,
        num_fake_observations=10000,
        quiet=False
        ):
    """Insert a fake observation record.
       Meant to be used with integration testing.
    """
    if not quiet:
        print("Inserting %s records into the observations data table"
              % num_fake_observations)

    for (lat, lng) in locations[:num_fake_observations]:

        observation_geom = func.ST_GeomFromText(
            'POINT({} {})'.format(lng, lat)
        )

        if not quiet:
            print('POINT({} {})'.format(lng, lat))

        _ = await session.add(Observation(
            school_id=usu_school_id,
            observed_lat=lat,
            observed_long=lng,
            observation_geom=observation_geom
        ))

if __name__ == '__main__':
    session = GearmapDbSession(env="integration_test")
    loop = asyncio.get_event_loop()
    task = loop.create_task(
        insert_fake_observations(session, quiet=False)
    )
    loop.run_until_complete(task)
    print("Done!")
