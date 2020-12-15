#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : gearmap_impl.py
author: chris rogers
why   : rest endpoint implementations
"""

# python modules
from functools import wraps

# 3rd party modules
from sqlalchemy import func
from sqlalchemy.exc import OperationalError
from shapely.geometry import Point

# gearmap modules
from db_models.Conference import Conference
from db_models.School import School
from db_models.Observation import Observation
from GearmapDbSession import GearmapDbSession
from utils.logger import logger
from DbConnectionError import DbConnectionError
from GearmapConfig import GearmapConfig
from SchoolNameResolver import SchoolNameResolver


def needs_db_connection(func, *args, **kwargs):
    """Decorator to gracefully fail DB calls."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            results = func(*args, **kwargs)
        except OperationalError as oe:
            raise DbConnectionError(
                "Unable to execute {}.  Reason: {}"
                .format(func.__name__, str(oe))
            )
        else:
            return results
    return wrapper


class GearmapImpl(object):
    """Interact with the database and show results.

    Define the way the rest endpoints interact with the
    database (through the SQLAlchemy and GeoAlchemy layers)
    and deliver the result sets back to the front end for rendering.
    """

    def __init__(self, new_env="dev", db_session=None):
        """Create the Impl object.

        Input args:
          db_session : dependency injection of whose db_session to use
                       this enables testing
        """
        self._APP_CFG = GearmapConfig()

        logger.name = __name__
        self._logger = logger

        assert isinstance(new_env, str), "Provided DB env for GearmapImpl " \
                                         "not a string."

        if not db_session:
            self.db_session = GearmapDbSession(env=new_env)
            self.db_env = new_env
        else:
            self.db_session = db_session
            self.db_env = self.db_session.which_env()

        self._logger.info("Created new instance of %s" % __name__)

    @needs_db_connection
    async def get_all_observations_in_polygon(self,
                                              polygon):
        """Retrieve all observations in a bounding box polygon."""
        try:
            # TRICKY: await means the object will be a coroutine
            #         until the event loop 'gets back' to it
            #         and can yield results.  Don't chain
            #         the filter() and all() functions directly.
            #         ALSO -- i'm not even sure this is helping...
            #         so i want to find out if the query object returns
            #         immediately and doesn't fetch from the db until
            #         instructed to do so with .fetch() or .fetch_all()
            #         or something
            result = await self.db_session.query(
                Observation,
                School
            )

            # TRICKY: Order of calls matter here.  Filter after
            #         join.
            result = result.join(
                School
            ).filter(
                func.ST_Contains(
                    polygon,
                    Observation.observation_geom
                )
            ).all()

        except DbConnectionError:
            raise DbConnectionError
        except Exception as e:
            self._logger.error(str(e))
            self.db_session.rollback()
            return {'status': 'fail', 'message': str(e)}

        self._logger.debug(f"Get School Observations in polygon; retrieved {len(result)} observations")
        return {'status': 'success', 'result': result}

    @needs_db_connection
    async def get_observations_by_school(self,
                                         school_names,
                                         env=None,
                                         polygon=None):
        """
        TODO: fill me out
        """
        if not isinstance(school_names, (list,)):
            school_names = [school_names]

        school_ids = list()

        if not env:
            env = self.db_env

        resolver = await SchoolNameResolver(env)
        #import ipdb; ipdb.set_trace(context=11)
        for s in school_names:
            if isinstance(s, str):
                # TRICKY: resolver returns a list of tuples
                #         each entry in the list is a school
                #         whose canonical name had the lowest
                #         levenshtein distance to the candidate
                #         school name.  there may be more than one
                resolved_schools = await resolver.resolve_school_names(
                    school_names
                )

                school_ids = [rs[0] for rs in resolved_schools]
            elif isinstance(s, int):
                # NOTE: Leaving this for when APIs hit this API
                #       and are smart enough to send the ID itself
                school_ids.append(s)
            else:
                err_msg = f"Unexpected school name (and type) provided: {s}; \
                           returning empty set"
                self._logger.error(err_msg)
                return {'status': 'fail', 'message': err_msg, 'result': []}

        try:
            query = await self.db_session.query(
                Observation
            )
            if not polygon:
                result = query.filter(
                    Observation.school_id.in_(school_ids)
                ).all()
            else:
                result = query.filter(
                    Observation.school_id.in_(school_ids),
                    func.ST_Contains(
                        polygon,
                        Observation.observation_geom
                    )
                ).all()

        except DbConnectionError:
            raise DbConnectionError
        except Exception as e:
            self.db_session.rollback()
            self._logger.error(str(e))
            return {'status': 'fail', 'message': str(e), 'result': []}

        return {'status': 'success', 'result': result}

    @needs_db_connection
    async def get_observations_by_conference(self,
                                             conference_ids,
                                             env=None,
                                             polygon=None):
        """
        TODO: fill me out
        """
        if env == None:
            env = self.db_env

        # TODO: we'll need a conference name resolver
        # as well, which will take an env arg

        if type(conference_ids) is not list:
            conference_ids = [conference_ids]

        try:
            # TODO: change this to an "in" query.
            if not polygon:
                query = await self.db_session.query(
                    Observation, School, Conference
                )

                result = query.filter(
                    School.id == Observation.school_id
                ).filter(
                    Conference.id == School.conference_id
                ).filter(
                    Conference.id.in_(conference_ids)
                ).all()

            else:
                query = await self.db_session.query(
                    Observation, School, Conference
                )

                result = query.filter(
                    School.id == Observation.school_id
                ).filter(
                    Conference.id == School.conference_id
                ).filter(
                    Conference.id.in_(conference_ids)
                ).filter(
                    func.ST_Contains(
                        polygon,
                        Observation.observation_geom
                    )
                ).all()

        except DbConnectionError:
            raise DbConnectionError
        except Exception as e:
            self.db_session.rollback()
            self._logger.error(str(e))
            return {'status': 'fail', 'message': str(e)}

        return {'status': 'success', 'result': result}

    @needs_db_connection
    async def process_new_observation(self, obsv_json):
        """Put a new observation in the database."""

        self._logger.info("Put a new School Observation")

        obsv_json['observation_geom'] = Point(
            float(obsv_json['observed_long']),
            float(obsv_json['observed_lat'])
        ).wkt

        new_observation = Observation.from_json(obsv_json)
        # TODO sanitize?  double check fields or something?
        try:
            result = await self.db_session.add(new_observation)
        except DbConnectionError:
            raise DbConnectionError
        except Exception as e:
            self.db_session.rollback()
            self._logger.error(str(e))
            return {'status': 'fail', 'message': str(e)}

        return {'status': 'success', 'result': result}
