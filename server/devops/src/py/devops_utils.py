#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file  : utils.py
author: chris rogers
why   : code re-use.  free floating functions.
"""

# python modules

# 3rd party modules
import docker

# gearmap modules


def rm_all(path, orig_dir):
    """Remove all files and subfolders (and their files and subfolders."""
    _ = [x.unlink() for x in path.iterdir() if x.is_file()]
    folders = [x for x in path.iterdir() if x.is_dir()]
    for folder in folders:
        rm_all(folder, orig_dir)
    if path != orig_dir:
        path.rmdir()


def stop_and_remove_db_container(DOCKER_CLIENT, DOCKER_CFG):
    """Stop and delete a container (in this instance, the db container)."""
    print("Stopping {}, then deleting..."
          .format(DOCKER_CFG.container_name))
    try:
        CONTAINER = DOCKER_CLIENT.containers.get(DOCKER_CFG.container_name)
    except docker.errors.NotFound:
        print('container not found, no need to stop or remove.  continuing...')
        return
    CONTAINER.stop()
    print("... container stopped")
    CONTAINER.remove()
    print("... and now removed.")
