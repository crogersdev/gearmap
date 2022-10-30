#!/bin/bash
set -e

cmd="$@"
timer="5"

until pg_isready -h ${GEARMAP_DBHOST} -p ${GEARMAP_DBPORT} 2>/dev/null; do 
  >&2 echo "Postgres is unavailable - sleeping for $timer seconds"
  sleep $timer
done

>&2 echo "Postgres is up - executing command"

export PYTHONPATH="/gearmap/devops/src/py:/gearmap/devops/src/db_setup:/gearmap/src/py:/gearmap/server/src/tests:/gearmap/common/src/py"

conda run -n gearmap_api python3 /gearmap/devops/src/py/GearmapDbBase.py
conda run -n gearmap_api python3 /gearmap/devops/src/db_setup/put_conferences_in_db.py
conda run -n gearmap_api python3 /gearmap/devops/src/db_setup/put_schools_in_db.py

conda run \
    --no-capture-output \
    -n gearmap_api \
    python3 ./src/py/api/app.py
