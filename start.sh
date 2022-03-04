#!/bin/bash
set -e
sh ./build.sh $1
docker-compose up