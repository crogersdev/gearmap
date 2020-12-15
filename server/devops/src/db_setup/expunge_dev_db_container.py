#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
file  : destroy_dev_db_container.py
author: chris rogers
why   : destroys gearmap api db container (dev)
        please don't run me manually.
        i will destroy the container, the image, and the volume
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
1.   stop and remove db container
2.   delete container image
3.   remove volume path
"""

# 0. housekeeping with the docker library
DOCKER_CLIENT = docker.from_env()
DOCKER_API_CLIENT = docker.APIClient(base_url=DOCKER_CFG.docker_sock)
TARGET_IMAGE = '{}:{}'.format(DOCKER_CFG.image_name, DOCKER_CFG.image_tag)
LOCAL_IMAGES = DOCKER_CLIENT.images.list()

# 1. stop and remove db container
print("stopping and removing container {}".format(DOCKER_CFG.container_name))
devops_utils.stop_and_remove_db_container(DOCKER_CLIENT, DOCKER_CFG)

# 2. delete container image
IMAGES = [x for x in LOCAL_IMAGES if TARGET_IMAGE in str(x)]
if IMAGES:
    print("removing docker image {}...".format(TARGET_IMAGE))
    DOCKER_CLIENT.images.remove(TARGET_IMAGE)

# 3. remove volume folder
VOL_PATH = Path(DOCKER_CFG.volume_path).joinpath(DOCKER_CFG.volume_folder)
if Path(DOCKER_CFG.volume_path).exists():
    try:
        devops_utils.rm_all(VOL_PATH, VOL_PATH)
    except OSError:
        raise OSError
    except Exception as ex:
        raise ex
