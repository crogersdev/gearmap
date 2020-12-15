#!/bin/bash

docker run \
    -d \
    --name gearmap_api \
    -e GEARMAP_DBHOST=172.17.0.2 \
    -p 5001:5001 \
    -v /gearmap:/gearmap \
    gearmap_api:1.0
