#!/usr/bin/env python
# -*- coding: utf-8 -*-

from GearmapConfig import GearmapConfig

cfg = GearmapConfig()


def drop_gearmap_schema(which_db='dev'):
    switch = {
        'dev': 'DROP SCHEMA IF EXISTS %s CASCADE;' % (
            cfg.DEV_DBCONFIG.dbschema
        ),
        'integration_test': 'DROP SCHEMA IF EXISTS %s CASCADE;' % (
            cfg.INTEGRATION_TEST_DBCONFIG.dbschema
        )
    }
    return switch.get(which_db, 'Error in drop_gearmap_schema sql statement')


def drop_school_table(which_db='dev'):
    switch = {
        'dev': 'DROP TABLE IF EXISTS %s CASCADE;' % (
            cfg.DEV_DBCONFIG.school_table
        ),
        'integration_test': 'DROP TABLE IF EXISTS %s CASCADE;' % (
            cfg.INTEGRATION_TEST_DBCONFIG.school_table
        )
    }
    return switch.get(
        which_db,
        'Error in drop_gearmap_school_table sql statement.'
    )


def drop_observation_table(which_db='dev'):
    switch = {
        'dev': 'DROP TABLE IF EXISTS %s CASCADE;' % (
            cfg.DEV_DBCONFIG.observation_table
        ),
        'integration_test': 'DROP TABLE IF EXISTS %s CASCADE;' % (
            cfg.INTEGRATION_TEST_DBCONFIG.observation_table
        )
    }
    return switch.get(
        which_db,
        'Error in drop_gearmap_observation_table sql statement.'
    )


def drop_conference_table(which_db='dev'):
    switch = {
        'dev': 'DROP TABLE IF EXISTS %s CASCADE;' % (
            cfg.DEV_DBCONFIG.conference_table
        ),
        'integration_test': 'DROP TABLE IF EXISTS %s CASCADE;' % (
            cfg.INTEGRATION_TEST_DBCONFIG.conference_table
        )
    }
    return switch.get(
        which_db,
        'Error in drop_conference_table sql statement.'
    )
