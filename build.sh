#!/usr/bin/env bash

set -x -e

docker-compose up -d --build
sleep 60

curl -X GET \
    http://localhost:8080/admin/demultiplex/health \
    -H 'Cache-Control: no-cache' \
    -H 'Content-Type: application/json'
