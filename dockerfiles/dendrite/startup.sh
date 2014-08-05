#!/bin/bash

if [ -z "$SSL" ]; then
  PORT=$(curl --silent http://172.17.42.1:2375/containers/$HOSTNAME/json | jq '.NetworkSettings.Ports."8448/tcp"[].HostPort')
else
        sed "s/config.port/443/g" -i /Dendrite/src/main/nodejs/ungit/bin/ungit
        sed "s|\"\"|\"/dendrite2\"|" -i /Dendrite/src/main/nodejs/ungit/bin/ungit
        sed -i "s/port:.*/port: 443,/g" /Dendrite/src/main/webapp/js/app.js;
fi
