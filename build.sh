#!/bin/bash
docker build -t twitter-profile-scoring:latest .
docker build -t nginx-basic-auth -f Dockerfile.nginx .