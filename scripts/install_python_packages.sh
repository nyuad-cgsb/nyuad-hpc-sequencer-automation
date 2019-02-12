#!/usr/bin/env bash

set -x -e
#find /home/airflow/pkgs -maxdepth 1 -mindepth 1 -type d | xargs -I {} "cd {} && pip --ignore-installed install ."
cd /home/airflow/pkgs/nyuad-cgsb-jira-client
pip install --ignore-installed .
