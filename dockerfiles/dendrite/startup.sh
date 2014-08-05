#!/bin/bash

if [ -z "$SSL" ]; then
  PORT=$(curl --silent http://172.17.42.1:2375/containers/$HOSTNAME/json | jq '.NetworkSettings.Ports."8448/tcp"[].HostPort')
  sed "s/port:.*/port: $PORT,/" -i /Dendrite/src/main/nodejs/ungit/source/config.js
else
  PORT=443
  sed "s/port:.*/port: $PORT,/" -i /Dendrite/src/main/nodejs/ungit/source/config.js
  sed "s/port:.*/port: $PORT,/" -i /Dendrite/src/main/webapp/js/app.js;
  sed "s|\"\"|\"/dendrite2\"|" -i /Dendrite/src/main/nodejs/ungit/bin/ungit
fi
