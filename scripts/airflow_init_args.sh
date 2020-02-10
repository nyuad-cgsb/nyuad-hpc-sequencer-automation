#!/usr/bin/env bash

#################################################################
# Arguments for Airflow initialization
# So far there is only the SSH connection to Dalma
#################################################################


# http://airflow.apache.org/cli.html#connections

#airflow connections [-h] [-l] [-a] [-d] [--conn_id CONN_ID]
#                    [--conn_uri CONN_URI] [--conn_extra CONN_EXTRA]
#                    [--conn_type CONN_TYPE] [--conn_host CONN_HOST]
#                    [--conn_login CONN_LOGIN] [--conn_password CONN_PASSWORD]
#                    [--conn_schema CONN_SCHEMA] [--conn_port CONN_PORT]

airflow connections -a \
    --conn_id "gencore@dalma.abudhabi.nyu.edu" \
    --conn_host "dalma.abudhabi.nyu.edu" \
    --conn_login "gencore" \
    --conn_type "SSH" \
    --conn_extra '{"key_file": "/root/.ssh/id_rsa", "no_host_key_check": true}'

# If for some reason you need to delete this -
# airflow connections -d \
#    --conn_id "gencore@dalma.abudhabi.nyu.edu"