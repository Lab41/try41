#!/bin/bash

if [ -z "$SSL" ]; then
	PORT=$(curl --silent http://172.17.42.1:2375/containers/$HOSTNAME/json | jq '.HostConfig.PortBindings."8448/tcp"[].HostPort')
	sed "s/config.port/$PORT/g" -i /Dendrite/src/main/nodejs/ungit/bin/ungit
else
        sed "s/config.port/443/g" -i /Dendrite/src/main/nodejs/ungit/bin/ungit
        sed "s|\"\"|\"/dendrite2\"|" -i /Dendrite/src/main/nodejs/ungit/bin/ungit
fi
