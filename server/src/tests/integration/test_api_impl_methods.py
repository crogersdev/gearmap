#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : test_api_impl_methods.py
author: chris rogers
why   : (integration) test rest endpoints (v1) for the gearmap middle-end
"""

# python modules

# 3rd party modules
from shapely.geometry import Point, Polygon
import pytest

# gearmap modules


@pytest.mark.asyncio
async def test_put_school_observation(db_session, gearmap_impl):
    gi = gearmap_impl

    from test_utils import fake_observations
    for fake_obsv in fake_observations:
        result = await gi.process_new_observation(fake_obsv)
        assert result['status'] == 'success'


@pytest.mark.asyncio
async def test_get_all_observations_in_polygon(db_session, gearmap_impl):
    gi = gearmap_impl

    from test_utils import polygons
    observations = await \
        gi.get_all_observations_in_polygon(
            polygons['most_of_the_usa']
        )

    # "POLYGON((x0 y0, x1 y1, ... x2, y2))"" becomes "x0 y0, x1, ... y2"
    lat_lng_str = polygons['most_of_the_usa'][9:-2]

    bbox_geom = Polygon([(float(lng), float(lat)) for lng, lat in [
        pair.split(' ') for pair in lat_lng_str.split(',')
    ]])

    assert observations['status'] == 'success'
    assert observations['result'] is not None and len(observations['result']) > 0

    outside_polygon = [
        o for o in observations['result'] if not bbox_geom.contains(
            Point(o[0].observed_long, o[0].observed_lat)
        )
    ]

    assert not outside_polygon


@pytest.mark.asyncio
async def test_get_observations_by_school(db_session, gearmap_impl):
    gi = gearmap_impl

    from test_utils import usu_school_id
    observations = await \
        gi.get_observations_by_school(
            "utah state",
            env=db_session.which_env()
        )

    assert observations['status'] == 'success'
    not_usu_observations = [
        o for o in observations['result'] if o.school_id != usu_school_id
    ]

    assert not not_usu_observations  # it's not NOT true! xD


@pytest.mark.asyncio
async def test_get_observations_by_school_in_polygon(db_session, gearmap_impl):
    gi = gearmap_impl

    from test_utils import usu_school_id, polygons
    observations = await \
        gi.get_observations_by_school(
            usu_school_id,
            polygon=polygons['most_of_the_usa'],
            env=db_session.which_env()
        )

    assert observations['status'] == 'success'

    not_usu_observations = [
        o for o in observations['result'] if o.school_id != usu_school_id
    ]

    assert not not_usu_observations  # it's not NOT true!

    # "POLYGON((x0 y0, x1 y1, ... x2, y2))"" becomes "x0 y0, x1, ... y2"
    lat_lng_str = polygons['most_of_the_usa'][9:-2]

    bbox_geom = Polygon([(float(lng), float(lat)) for lng, lat in [
        pair.split(' ') for pair in lat_lng_str.split(',')
    ]])

    outside_polygon = [
        o for o in observations['result'] if not bbox_geom.contains(
            Point(o.observed_long, o.observed_lat)
        )
    ]

    assert not outside_polygon


@pytest.mark.asyncio
async def test_get_observations_by_conference(db_session, gearmap_impl):
    gi = gearmap_impl

    from test_utils import mwc_conf_id, mac_conf_id

    observations = await \
        gi.get_observations_by_conference(
            [mwc_conf_id, mac_conf_id],
            env=db_session.which_env()
        )

    assert observations['status'] == 'success'

    conf_ids = {mwc_conf_id, mac_conf_id}
    for o in observations['result']:
        assert o.Conference.id in conf_ids


@pytest.mark.asyncio
async def test_get_observations_by_conference_in_polygon(db_session, gearmap_impl):
    gi = gearmap_impl

    from test_utils import mwc_conf_id, polygons

    observations = await \
        gi.get_observations_by_conference(
            mwc_conf_id,
            polygon=polygons['most_of_the_usa'],
            env=db_session.which_env()
        )

        # "POLYGON((x0 y0, x1 y1, ... x2, y2))"" becomes "x0 y0, x1, ... y2"
    lat_lng_str = polygons['most_of_the_usa'][9:-2]

    bbox_geom = Polygon([(float(lng), float(lat)) for lng, lat in [
        pair.split(' ') for pair in lat_lng_str.split(',')
    ]])

    outside_polygon = [
        o for o in observations['result'] if not bbox_geom.contains(
            Point(o[0].observed_long, o[0].observed_lat)
        )
    ]

    assert observations['status'] == 'success'
    for o in observations['result']:
        assert o.Conference.id == mwc_conf_id
    assert not outside_polygon
