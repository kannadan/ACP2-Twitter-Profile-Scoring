#!/bin/bash
set -e
echo "Building"
proxy=$1
if [ ! -z $proxy ]; then
    build_args="--build-arg PROXY=$proxy"
else
    build_args=""
fi
docker build $build_args -t twitter-profile-scoring:latest .
docker build $build_args -t nginx-basic-auth -f Dockerfile.nginx .