#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : conftest.py
author: chris rogers
why   : setup and tear down for pytest fixtures
"""

# python modules
import asyncio
import pytest

# 3rd party modules

# gearmap modules
from drop_all_data_from_db import destroy_them_all
from put_conferences_in_db import add_conferences
from put_schools_in_db import add_schools

from api.GearmapImpl import GearmapImpl
from GearmapConfig import GearmapConfig
from GearmapDbBase import create_all
from GearmapDbSession import GearmapDbSession

CFG = GearmapConfig()


@pytest.fixture(scope="session")
async def db_session(request):
    """ TODO: fill me in """
    db_session = GearmapDbSession(env='integration_test')

    def teardown():
        """ finalizer function that runs
            at the end of all tests for the session that
            uses this fixture

            can't be async because of pytest but has to await the task,
            so use asyncio.run
        """
        asyncio.run(destroy_them_all(db_session, quiet=True))

    await create_all(db_session, quiet=True)
    await add_conferences(db_session, quiet=True)
    await add_schools(db_session, quiet=True)

    request.addfinalizer(teardown)

    return db_session


@pytest.fixture(scope="session")
def gearmap_impl(db_session):
    # TRICKY: I have no idea how pytest is able to hook up the 
    # db_session arg here with the previous fixture... but it does.
    gi = GearmapImpl(db_session=db_session)
    return gi


@pytest.yield_fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
