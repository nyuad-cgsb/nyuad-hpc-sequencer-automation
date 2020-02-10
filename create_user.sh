#!/usr/bin/env bash

##############################################
# This script is only here for record keeping
# The user is already created

# Must be sudo or an admin user

useradd airflow
sudo su - airflow
mkdir .ssh
cd .ssh

ssh-keygen id_rsa -N
cat id_rsa.pub >> authorized_keys

# Then copy the id_rsa to the local .ssh folder and chmod 400 it
