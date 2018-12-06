#!/usr/bin/env bash

cd ..
rsync -avz -e 'ssh -p 4410' nyuad-hpc-sequencer-automation "jdr400@10.230.12.10:/home/jdr400/DEPLOY"
ssh -p 4410 jdr400@10.230.12.10 "cd /home/jdr400/DEPLOY/nyuad-hpc-sequencer-automation/ && docker-compose restart"
