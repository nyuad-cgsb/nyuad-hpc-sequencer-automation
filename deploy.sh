#!/usr/bin/env bash

# Check out what's happening at
# http://10.230.12.10:8080

set -x -e

DEPLOY_DIR=$(PWD)
DEPLOY_IP="10.230.12.10"
DEPLOY_USER="airflow"
DEPLOY_KEY=".ssh/airflow_user"

###############################################################################
# Bring up the docker-compose instance to build the front end
###############################################################################
docker-compose stop
#docker-compose build
#docker-compose up -d

###############################################################################
# Permissions on SSH Keys
# SSH is picky about permissions and will cause scripts to fail if the permissions are not correct
###############################################################################

chmod 400 .ssh/*

###############################################################################
# Build additional front end functionality for plugins
###############################################################################
# move this to the docker container
cd www-sequencer-automation
#docker-compose exec www_sequencer_automation bash -c "ng build --prod  --output-hashing none --configuration=production --output-path /home/node/plugins/static/"

###############################################################################
# Done with docker-compose. Bring it down
###############################################################################
#docker-compose stop

###############################################################################
# Build additional front end functionality for plugins
###############################################################################
cd ${DEPLOY_DIR}

# Ensure directories exist before beginning deploy

ssh -p 4410 -i ${DEPLOY_DIR}/${DEPLOY_KEY} \
    ${DEPLOY_USER}@${DEPLOY_IP} \
    mkdir -p /home/${DEPLOY_USER}/DEPLOY/nyuad-hpc-sequencer-automation

# Really weird things happen if you move DAGs around, but don't clean up

ssh -p 4410 -i ${DEPLOY_DIR}/${DEPLOY_KEY} \
    ${DEPLOY_USER}@${DEPLOY_IP} \
    "cd /home/${DEPLOY_USER}/DEPLOY/ && rm -rf nyuad-hpc-sequencer-automation/dags"

cd ..

rsync -avz -e "ssh -p 4410 -i ${DEPLOY_DIR}/${DEPLOY_KEY}" \
    --exclude "*node_modules*" \
    --exclude "*.git*" \
    --exclude "airflow/logs" \
    --exclude "airflow/airflow-webserver.pid" \
    nyuad-hpc-sequencer-automation \
    "${DEPLOY_USER}@${DEPLOY_IP}:/home/${DEPLOY_USER}/DEPLOY"

cd ${DEPLOY_DIR}

ssh -p 4410 -i ${DEPLOY_DIR}/${DEPLOY_KEY} \
    ${DEPLOY_USER}@${DEPLOY_IP} \
    "cd /home/${DEPLOY_USER}/DEPLOY/nyuad-hpc-sequencer-automation/ && docker-compose stop; docker-compose build; docker-compose up -d --remove-orphans"

# Leave in the sleep commands!
# The first time around the database does not get populated all the way
# Restarting fixes this
sleep 60
ssh -p 4410 -i ${DEPLOY_DIR}/${DEPLOY_KEY} \
    ${DEPLOY_USER}@${DEPLOY_IP} "cd /home/${DEPLOY_USER}/DEPLOY/nyuad-hpc-sequencer-automation/ && docker-compose restart"
sleep 30
ssh -p 4410 -i ${DEPLOY_DIR}/${DEPLOY_KEY} \
    ${DEPLOY_USER}@${DEPLOY_IP} "cd /home/${DEPLOY_USER}/DEPLOY/nyuad-hpc-sequencer-automation/ && docker-compose logs --tail 100 airflow_sequencer_automation_webserver"




# Trouble shooting
# ssh -p 4410 jdr400@10.230.12.10 "cd /home/jdr400/DEPLOY/nyuad-hpc-sequencer-automation/ && docker-compose stop; docker-compose rm -f -v"
# ssh -p 4410 jdr400@10.230.12.10 "docker system prune -f -a"
