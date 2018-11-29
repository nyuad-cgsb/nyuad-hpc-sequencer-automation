#!/usr/bin/env bash

cd /docker-entrypoint-initdb.d
mysql -uroot -ppassword < 000-init.sql 

