#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : create_dev_db_container.py
author: chris rogers
why   : runs inside the postgis container and populates the db.
        please don't run me manually.
        assumes you want to do this from a fresh
        system.  should be able to handle being run, non destructively,
        even if everything's already been run.  (idempotent?)
"""

# python modules
from pathlib import Path

# 3rd party modules
import docker

# gearmap modules
import devops_utils
from GearmapConfig import GearmapConfig


CFG = GearmapConfig()
DOCKER_CFG = CFG.DEV_DOCKER_CFG

"""
plan of attack
1.  check if image is there.  if not, pull.
2.  make sure data volume is there
2a.   clear it out if necessary
3.  create container
4.  start container
"""

# 0. housekeeping with the docker library
DOCKER_CLIENT = docker.from_env()
DOCKER_API_CLIENT = docker.APIClient(base_url=DOCKER_CFG.docker_sock)
TARGET_IMAGE = '{}:{}'.format(DOCKER_CFG.image_name, DOCKER_CFG.image_tag)
LOCAL_IMAGES = DOCKER_CLIENT.images.list()

# 1. check if image exists on systems.  if not, pull
print("System is configured to look for docker image {}".format(TARGET_IMAGE))
print("Proceeding with docker container checks...")

IMAGES = [x for x in LOCAL_IMAGES if TARGET_IMAGE in str(x)]
if not IMAGES:
    print("{} image not found.  Pulling... ".format(TARGET_IMAGE))
    DOCKER_API_CLIENT.pull(DOCKER_CFG.image_name, tag=DOCKER_CFG.image_tag)
    print("{} pulled.".format(TARGET_IMAGE))
    # use list of images later, so update
    IMAGES = [x for x in LOCAL_IMAGES if TARGET_IMAGE in str(x)]
else:
    print("{} found.  Checking for running containers...".format(TARGET_IMAGE))
    devops_utils.stop_and_remove_db_container(DOCKER_CLIENT, DOCKER_CFG)

# 2. make sure /data/gearmap_postgis/ exists for container mounted volume
VOL_PATH = Path(DOCKER_CFG.volume_path).joinpath(DOCKER_CFG.volume_folder)
print("Checking to see if {} exists...".format(VOL_PATH))
if Path(DOCKER_CFG.volume_path).exists():
    try:
        VOL_PATH.mkdir(mode=0o755, parents=True, exist_ok=True)
    except PermissionError:
        raise PermissionError
    except Exception as ex:
        raise ex
else:
    E_STR = 'Unable to find {}; please create and re-run.' \
            .format(DOCKER_CFG.volume_path)
    raise OSError(E_STR)

# 2a. rm dirs and data if necessary
print('Removing all files and subfolders from {}...'.format(str(VOL_PATH)))
try:
    devops_utils.rm_all(VOL_PATH, VOL_PATH)
except OSError:
    raise OSError
except Exception as ex:
    raise ex

# 3. create container
print('Creating container...')

GEARMAP_API_DB_HOST_CONFIG = DOCKER_API_CLIENT.create_host_config(
    binds=DOCKER_CFG.volume_bindings,
    port_bindings=DOCKER_CFG.port_bindings,
)

GEARMAP_API_DB_CONTAINER = DOCKER_API_CLIENT.create_container(
    name=DOCKER_CFG.container_name,
    image=TARGET_IMAGE,
    ports=DOCKER_CFG.ports,
    host_config=GEARMAP_API_DB_HOST_CONFIG
)

GEARMAP_API_DB_CONTAINER.update(restart_policy=DOCKER_CFG.restart_policy)

print('{} created!'.format(DOCKER_CFG.container_name))

# 4. run container
DOCKER_API_CLIENT.start(GEARMAP_API_DB_CONTAINER)
print('{} is now running!'.format(DOCKER_CFG.container_name))
