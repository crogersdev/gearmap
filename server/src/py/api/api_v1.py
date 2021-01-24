#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : api_v1.py
author: chris rogers
why   : rest endpoints (v1) for the gearmap middle-end
"""

# python modules
import shapely.wkt
import shapely.geometry as shapely_geometry
from geojson import Polygon

# 3rd party modules
import aiohttp_cors
from aiohttp import web

# gearmap modules
import observations_utils
from utils.logger import logger
from DbConnectionError import DbConnectionError
from GearmapConfig import GearmapConfig
from GearmapResponse import GearmapResponse

API_CFG = GearmapConfig()
routes = web.RouteTableDef()

def db_connection_error_msg():
    return GearmapResponse(
        status="fail",
        data={
            "data": observations_utils.EMPTY_GEOJSON,
            "num_observations": 0
        },
        message="Unable to talk to database.  Please consult server logs."
    ).to_json()


@routes.get('/ping')
async def ping(request):
    logger.info("ping request received")
    return web.Response(text='Pong!')


@routes.post('/observations')
async def get_all_observations_in_polygon(request):
    body = await request.json()
    logger.debug(f"/observations hit with {body}")
    polygon = body.get('bbox', None)

    if not polygon:
        return web.HTTPBadRequest(
            text='Unable to parse requested polygon for observation retrieval'
        )

    geometry = shapely.wkt.loads(polygon)
    geo_json = shapely_geometry.mapping(geometry)

    # NOTE: we force the creation of a Polygon instance
    #       to guarantee our incoming polygon is a
    #       GeoJSON polygon.
    _ = Polygon(geo_json['coordinates'])

    GearmapImpl = request.app.get('GearmapImpl')

    try:
        observations = await GearmapImpl.get_all_observations_in_polygon(
            polygon=polygon
        )
    except DbConnectionError:
        return web.Response(
            db_connection_error_msg(),
            content_type='application/json'
        )

    logger.debug(f"{len(observations['result'])} results returned")

    if observations['status'] == 'fail':
        return web.json_response(
            GearmapResponse(
                status='fail',
                data={},
                message=observations.get('result', 'No observations results returned')
            ).to_json()
        )

    return web.json_response(
        GearmapResponse(
            status='success',
            data={
                "data": observations_utils.to_geojson(
                    observations['result']
                ),
                "num_observations": len(observations['result'])
            }
        ).to_json()
    )


@routes.post('/observations_by_schools')
async def get_observations_by_school(request):
    body = await request.json()
    logger.debug(f"/observations_by_schools hit with {body}")

    school_names = body.get('school_names', None)
    polygon = body.get('bbox', None)

    if not school_names:
        return web.HTTPBadRequest(
                text='No school names to search for supplied'
            )

    GearmapImpl = request.app.get('GearmapImpl')

    try:
        observations = await GearmapImpl.get_observations_by_school(
            school_names=school_names,
            polygon=polygon
        )
    except DbConnectionError:
        return web.json_response(
            db_connection_error_msg(),
            content_type='application/json',
            status=200
        )

    logger.debug(f"{len(observations['result'])} results returned")

    return web.json_response(
        GearmapResponse(
            status='success',
            data={
                'data': observations_utils.to_geojson(observations),
                'num_observations': len(observations['result'])
            }
        ).to_json()
    )


@routes.post('/observations_by_conference')
async def get_observations_by_conference(request):
    body = await request.json()
    logger.debug(f"/observations_by_conference hit with {body}")

    conference_ids = body.get('conference_ids', None)
    polygon = body.get('bbox', None)

    GearmapImpl = request.app.get('GearmapImpl')

    try:
        observations = await GearmapImpl.get_school_observations(
            conference_ids=conference_ids,
            polygon=polygon
        )
    except DbConnectionError:
        return web.Response(
            db_connection_error_msg(),
            content_type='application/json'
        )

    logger.debug(f"{len(observations['result'])} results returned")

    return web.json_response(
        GearmapResponse(
            status='success',
            data={
                'data': observations_utils.to_geojson(observations),
                'num_observations': len(observations['result'])
            }
        )
    )


@routes.post('/new_observation')
async def process_new_observation(request):
    body = await request.json()
    logger.debug(f"/new_observation endpoint hit with {body}")

    for observation in body:
        school_observed = observation.get('school', None)
        location_long = observation.get('location_long', None)
        location_lat = observation.get('location_lat', None)
        school_id = observation.get('school_id', None)
        if not all([school_observed, location_long, location_lat, school_id]):
            return web.HTTPBadRequest(
                text='Unable to parse new observation request, ' +
                     'missing required field: school_observed, ' +
                     'location longitude, school_id, or location latitude.'
            )

        GearmapImpl = request.app.get('GearmapImpl')

        try:
            status = await GearmapImpl.put_school_observation(observation)
        except DbConnectionError:
            return web.Response(
                db_connection_error_msg(),
                content_type='application/json'
            )

    return web.json_response(
        GearmapResponse(
            status='success',
            data={
                "status": status
            }
        )
    )


def create_gearmap_app(loop):
    gearmap_app = web.Application(loop=loop)

    # TRICKY: Please remove me when this is no longer in dev.
    cors = aiohttp_cors.setup(gearmap_app)
    for r in routes:
        resource = cors.add(gearmap_app.router.add_resource(r.path))
        cors.add(
            resource.add_route(r.method, r.handler),
            {'*': aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers=("X-Custom-Server-Header",),
                allow_headers=("X-Requested-With", "Content-Type"),
                max_age=3600)
             }
        )
    gearmap_app.router.add_routes(routes)
    return gearmap_app
