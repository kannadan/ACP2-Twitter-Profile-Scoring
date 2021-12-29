#!/bin/bash
if [ ! -f .env ]; then
    echo ".env file does not exist, copy .env.dist as .env and fill the values"
    exit 1
fi
source ./.env

if [ -z $DEPLOY_SSH_USER ]; then
    echo "DEPLOY_SSH_USER not set"
    exit 1
fi
if [ -z $DEPLOY_SSH_HOST ]; then
    echo "DEPLOY_SSH_HOST not set"
    exit 1
fi
if [ -z $DEPLOY_SSH_PORT ]; then
    DEPLOY_SSH_PORT=22
fi
BASEDIR="/home/${DEPLOY_SSH_USER}"
ssh -p $DEPLOY_SSH_PORT ${DEPLOY_SSH_USER}@${DEPLOY_SSH_HOST} """
    sudo -u docker ${BASEDIR}/deploy.sh
"""
