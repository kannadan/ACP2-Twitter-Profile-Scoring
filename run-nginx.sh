#!/bin/sh

envsubst < nginx-basic-auth.conf > /etc/nginx/conf.d/default.conf
htpasswd -c -b /etc/nginx/.htpasswd $BASIC_USERNAME $BASIC_PASSWORD
echo "Starting nginx"
nginx -g "daemon off;"
