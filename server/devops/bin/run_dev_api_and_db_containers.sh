#!/bin/bash

# don't forget to run this guy on a new machine:
# pythonpip3 install -r ../conda.txt

# exit on first error.  this gives us error checking for free,
# as we don't need to check the output of a previous call
# before moving onwards.
set -o errexit

source /gearmap/devops/set_env.sh

echo "prepping host for dev db setup..."
python3 /gearmap/devops/src/db_setup/prep_host_for_dev_db.py