#!/usr/bin/env bash

set -x -e

docker-compose build
docker-compose up -d

scripts/wait-for-it.sh -p 8080 -h localhost -- echo "Webserver is up"

curl -X GET \
    http://localhost:8080/admin/demultiplex/health \
    -H 'Cache-Control: no-cache' \
    -H 'Content-Type: application/json'


# Just show some logs here
docker-compose logs --tail 100 airflow_sequencer_automation_webserver
docker-compose logs --tail 100 airflow_sequencer_automation_scheduler
docker-compose logs --tail 100 airflow_sequencer_automation_worker
