#!/bin/sh
envsubst < nginx-basic-auth.conf > /etc/nginx/conf.d/default.conf
htpasswd -c -b /etc/nginx/.htpasswd $BASIC_USERNAME $BASIC_PASSWORD
cat /etc/nginx/conf.d/default.conf
echo "Starting nginx proxy"
nginx -g "daemon off;"
