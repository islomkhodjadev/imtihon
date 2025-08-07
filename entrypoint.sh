#!/bin/sh
# entrypoint.sh

echo "Starting NGINX with env: SERVER_NAME=$SERVER_NAME PORT_NGINX=$PORT_NGINX"

# Substitute environment variables in template and run nginx
envsubst '${SERVER_NAME} ${PORT_NGINX}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

exec nginx -g 'daemon off;'
