#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : observations_utils.py
author: chris rogers
why   : perform operations on observations
"""

# python modules

# 3rd party modueles

# gearmap modules


def to_geojson(observations):
    """Convert list of observations to a jsonblob of geojson"""
    # TODO(crogers): pagination

    if type(observations) is not list:
        observations = list(observations)

    #TODO: replace with fancy list comprehension
    feature_list = []
    import ipdb; ipdb.set_trace(context=11)
    for o in observations:
        (observation, school) = o
        feature_list.append({
            "type": "Feature",
            "properties": {
                "icon": school.marker,
                "title": school.school,
            },
            "geometry": {
                "type": "Point", "coordinates": [
                    "{0:.2f}".format(observation.observed_long),
                    "{0:.2f}".format(observation.observed_lat)
                ]
            }
        })

    '''
    feature_list = [
        {
            "type": "Feature",
            "properties": {
                "icon": o.school.marker,
                "title": o.school.school,
            },
            "geometry": {
                "type": "Point", "coordinates": [
                    "{0:.2f}".format(o.observed_long), 
                    "{0:.2f}".format(o.observed_lat)
                ]
            }
        } for o in observations]
    '''
    observations_geojson = {
        "type": "FeatureCollection", 
        "features": feature_list
    }

    return observations_geojson


EMPTY_GEOJSON = {
    "type": "FeatureCollection",
    "features": []
}
