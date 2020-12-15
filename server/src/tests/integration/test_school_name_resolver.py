#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : test_school_name_resolver.py
author: chris rogers
why   : (integration) test the school name resolver
"""

# python modules

# 3rd party modules
import pytest

# gearmap modules
from SchoolNameResolver import SchoolNameResolver


@pytest.mark.asyncio
async def test_resolver_retrieve_school_names(db_session, gearmap_impl):
    resolver = await SchoolNameResolver(db_session.which_env())
    await resolver._build_team_name_dict()
    assert len(resolver.team_and_ids.keys()) >= 100


@pytest.mark.asyncio
async def test_resolver_resolve_name(db_session, gearmap_impl):
    resolver = await SchoolNameResolver(db_session.which_env())
    await resolver.resolve_school_names(['usu'])
