#!/usr/bin/env bash

set -x -e

docker-compose up -d --build  --abort-on-container-exit

scripts/wait-for-it.sh -p 8080 -h localhost -- echo "Webserver is up"

curl -X GET \
    http://localhost:8080/admin/demultiplex/health \
    -H 'Cache-Control: no-cache' \
    -H 'Content-Type: application/json'
