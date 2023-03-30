#!/bin/bash

THIS_DIR=$(dirname $(readlink -f $0))

/etc/init.d/cron start & 

python3 ${THIS_DIR}/WebApp.py
