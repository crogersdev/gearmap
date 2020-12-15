#!/usr/bin/env bash

# please run me in a container where everything is mounted
# under /gearmap

python3 /gearmap/devops/src/db_setup/drop_all_data_from_dev_db.py
#TODO change to event driven rather than sleeping
sleep 4
python3 /gearmap/devops/src/db_setup/destroy_dev_db_container.py
