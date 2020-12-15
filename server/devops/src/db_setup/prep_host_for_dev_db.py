#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : prep_host_for_dev_db.py
author: chris rogers
why   : runs prior to postgis dev db container is setup
        makes sure data dir for the db is configurable
        from GearmapConfig
        requires that the folder be created.
        why don't you create it from code?
        because i don't know that that's a good idea. 
"""

# python modules
from pathlib import Path

# 3rd party modules

# gearmap modules
import devops_utils
from GearmapConfig import GearmapConfig


CFG = GearmapConfig()
DOCKER_CFG = CFG.DEV_DOCKER_CFG

"""
plan of attack
1.  ensure host dir is there for mounting
2.  clear it out if necessary
"""

# 1. make sure /data/gearmap_postgis/ exists for container mounted volume
VOL_PATH = Path(DOCKER_CFG.volume_path).joinpath(DOCKER_CFG.volume_folder)
print("Checking to see if {} exists...".format(VOL_PATH))
if not Path(DOCKER_CFG.volume_path).exists():
    try:
        VOL_PATH.mkdir(mode=0o755, parents=True, exist_ok=True)
    except PermissionError:
        raise PermissionError
    except Exception as ex:
        raise ex

# 2. rm dirs and data if necessary
print('Removing all files and subfolders from {}...'.format(str(VOL_PATH)))
try:
    devops_utils.rm_all(VOL_PATH, VOL_PATH)
except OSError:
    raise OSError
except Exception as ex:
    raise ex
