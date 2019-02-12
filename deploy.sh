#!/usr/bin/env bash


set -x -e

###############################################################################
# Build additional front end functionality for plugins
###############################################################################
cd www-sequencer-automation
ng build --prod  --output-hashing none --configuration=production --output-path ../plugins/static/

###############################################################################
# Build additional front end functionality for plugins
###############################################################################
cd ../..
rsync -avz -e 'ssh -p 4410' nyuad-hpc-sequencer-automation "jdr400@10.230.12.10:/home/jdr400/DEPLOY"
#ssh -p 4410 jdr400@10.230.12.10 "cd /home/jdr400/DEPLOY/nyuad-hpc-sequencer-automation/ && docker-compose stop; docker-compose rm -f; docker-compose up -d"
ssh -p 4410 jdr400@10.230.12.10 "cd /home/jdr400/DEPLOY/nyuad-hpc-sequencer-automation/ && docker-compose restart"
