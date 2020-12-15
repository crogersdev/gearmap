#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : test_api_impl_methods.py
author: chris rogers
why   : (unit) test rest endpoints (v1) for the gearmap middle-end
"""

# python modules

# 3rd party modules
import asynctest
import pytest

# gearmap modules
from api.GearmapImpl import GearmapImpl

#TRICKY: I have had to fully qualify the path to the GearmapDbSession
#        methods via module.class_name.method_name
#        I find this preferable to including the module and
#        referring to it as an included object.


@pytest.mark.asyncio
@asynctest.patch('GearmapDbSession.GearmapDbSession.query',
                 new_callable=asynctest.CoroutineMock)
async def test_get_observations_bad_polygon(db_session_query):
    """
    Test: Use a bad polygon when you get all observations.
    Expectations: Fails.
    Rationale: n/a
    """

    gearmap_impl = GearmapImpl()
    polygon = 'bad polygon'

    mocked_db_actions = await gearmap_impl.get_all_observations_in_polygon(polygon)

    for func in ['query', 'join', 'filter', 'all']:
        assert func in str(mocked_db_actions['result'])


@pytest.mark.asyncio
async def test_process_new_observation_empty_body():
    """
    Test: Put an empty observation in.
    Expectations: Fails with TypeError.
    Rationale: n/a
    """
    gearmap_impl = GearmapImpl()

    with pytest.raises(KeyError):
        await gearmap_impl.process_new_observation({})


@pytest.mark.asyncio
@asynctest.patch('GearmapDbSession.GearmapDbSession.add',
                 new_callable=asynctest.CoroutineMock)
async def test_process_new_observation(mocked_add_observation):
    """
    Test: Put an observation in the database.
    Expectations: Success.
    Rationale: This test uses the put_school_observation() method in 
                GearmapImpl to add an observation; so we're testing
                the ability of the Observation class to de-serialize
                the JSON we give it and inflate a new Observation
                class instance.

                Q. Why not just put in a test for the Observation class?
                A. I suppose we could.
    """
    fake_data = {
        'observed_lat': 1.23,
        'observed_long': -1.23,
        'observation_geom': 'fake geometry goes here',
        'school_id': 1234
    }
    gearmap_impl = GearmapImpl()
    mocked_add_observation.return_value = 'success'
    result = await gearmap_impl.process_new_observation(fake_data)

    assert result['status'] == 'success'

@pytest.mark.asyncio
async def test_get_school_observations_in_polygon(event_loop):
    #TODO: Implement me!!!
    pass