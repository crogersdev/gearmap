#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
from os import environ


class GearmapConfig(object):
    def __init__(self):
        self.db_cfg = namedtuple('db_cfg', 'dbhost dbport dbname dbuser '
                                 'dbpasswd dbschema  '
                                 'conference_table '
                                 'school_table '
                                 'observation_table '
                                 'observations_test_data_table ')

        self.INIT_DEV_DBCONFIG = self.db_cfg(
            dbhost=environ.get('GEARMAP_DBHOST', 'db'),
            dbport=environ.get('GEARMAP_DBPORT', '5432'),
            dbname=environ.get('GEARMAP_DBNAME', 'postgres'),
            dbpasswd=environ.get('GEARMAP_DBPASS', 'postgres'),
            dbuser=environ.get('GEARMAP_DBUSER', 'postgres'),
            dbschema=environ.get('GEARMAP_DBSCHEMA', 'gearmap'),
            conference_table='conferences',
            school_table='schools',
            observations_test_data_table='observations_test_data',
            observation_table='observations',
        )

        self.DEV_DBCONFIG = self.db_cfg(
            dbhost=environ.get('GEARMAP_DBHOST', 'db'),
            dbport=environ.get('GEARMAP_DBPORT', '5432'),
            dbname=environ.get('GEARMAP_DBNAME', 'postgres'),
            dbpasswd=environ.get('GEARMAP_DBPASS', 'postgres'),
            dbuser=environ.get('GEARMAP_DBUSER', 'postgres'),
            dbschema=environ.get('GEARMAP_DBSCHEMA', 'gearmap'),
            conference_table='conferences',
            school_table='schools',
            observations_test_data_table='observations_test_data',
            observation_table='observations',
        )

        self.INTEGRATION_TEST_DBCONFIG = self.db_cfg(
            dbhost=environ.get('GEARMAP_INTEGRATION_TEST_DBHOST', 'db'),
            dbport=environ.get('GEARMAP_INTEGRATION_TEST_DBPORT', '5432'),
            dbname='gearmap_integration_test',
            dbpasswd=environ.get('PGPASSWORD', 'postgres'),
            dbuser='postgres',
            dbschema='gearmap',
            conference_table='conferences',
            school_table='schools',
            observations_test_data_table='observations_test_data',
            observation_table='observations',
        )

        self.docker_cfg = namedtuple('docker_cfg',
                                     'container_name image_name image_tag '
                                     'volume_path volume_folder volumes '
                                     'volume_bindings ports port_bindings '
                                     'docker_sock restart_policy')
        self.DEV_DOCKER_CFG = \
            self.docker_cfg(
                container_name='gearmap_api_db',
                image_name='mdillon/postgis',
                image_tag='10-alpine',

                # used for filesystem prep
                volume_path='/data/gearmap_db',
                volume_folder='gearmap_postgis',

                # used to create the container volume bindings
                volumes=['/data/gearmap_db/gearmap_postgis'],
                volume_bindings={
                    '/data/gearmap_db/gearmap_postgis': {
                        'bind': '/data',
                        'mode': 'rw',
                    },
                },

                ports=[5432],
                port_bindings={5432: 5432},

                docker_sock='unix://var/run/docker.sock',

                restart_policy={
                    'MaximumRetryCount': 0,
                    'Name': 'always',
                },
            )

        self.app_cfg = namedtuple(
            'app_cfg',
            'app_name api_container_name '
            'db_container_name app_log_filename '
            'app_logger_name app_logger_path'
        )

        self.DEV_APPCONFIG = self.app_cfg(
            app_name='gearmap',
            api_container_name='gearmap_postgis',
            db_container_name='gearmap_api',
            app_log_filename='gearmap_app.log',
            app_logger_name='gearmap_app',
            app_logger_path='/gearmap/logs'
        )

        self.webapp_cfg = namedtuple(
            'webapp_cfg',
            'port'
        )

        self.DEV_WEBAPPCONFIG = self.webapp_cfg(port=5001)
