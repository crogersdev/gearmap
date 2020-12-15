#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : SchoolNameResolver.py
author: chris rogers
why   : provides a way to retrieve a school id given a
        human specified school name

        e.g. 'vatech' -> 'Virginia Tech University'
        so the back end can recognize
"""

# python modules
from abc import ABCMeta
from abc import abstractmethod
from collections import defaultdict

# 3rd party modules
import Levenshtein as lev

# gearmap modules
from db_models.Conference import Conference
from db_models.School import School
from GearmapDbSession import GearmapDbSession


class AsyncSchoolNameResolver(metaclass=ABCMeta):
    """
    I found this pattern on the web.  This parent class allows async
    init's.  The problem is that __init__()'s can't return anything
    other than `None`.  And if we have a coroutine in the ctor,
    then the return value will be the coroutine object.

    To circumvent, we play a fancy little game of overriding the
    super class init by awaiting the newly created object's __init__
    method, which allows us to await the coroutine and then return
    newly created instance
    """
    async def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        await instance.__init__(*args, **kwargs)
        return instance

    @abstractmethod
    async def __init__(self):
        pass


class SchoolNameResolver(AsyncSchoolNameResolver):
    """
    Returns an id that the gearmap db will recognize.

    Takes in any kind of description of a school, a conference,
    an organizational entity, etc...  As the usage of this app
    grows beyond college football, I'll want to be able to resolve
    things like "hotspurs" to "tottenham hotspurs" or something.
    "psg" to "Paris Saint Germain" and such.
    """

    async def __init__(self, new_env="dev", db_session=None):

        self.team_and_ids = {}
        if not db_session:
            self.db_session = GearmapDbSession(env=new_env)
        else:
            self.db_session = db_session

        await self._build_team_name_dict()

    async def _build_team_name_dict(self):
        """
        Hit the db, get all the team names, get their IDs, and
        return it as a dict

        we're going to need to iterate through each school and compare it to
        the candidate to find our best guess
        """

        schools_query_resp = await self.db_session.query(School)
        schools = schools_query_resp.all()
        self.team_and_ids = dict([(s.id, s.school) for s in schools])

    async def resolve_school_names(self, school_names):
        """
        Resolve the name using some voodoo such that its
        resolved name matches what we have in the database.
        """

        if not isinstance(school_names, list):
            school_names = [school_names]

        scores = defaultdict(list)

        for s in school_names:
            for (school_id, canonical_name) in self.team_and_ids.items():
                ld = lev.distance(s, canonical_name)
                scores[ld].append((school_id, canonical_name))

        min_score = min(scores.keys())
        return scores[min_score]
