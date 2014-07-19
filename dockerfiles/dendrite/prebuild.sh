#!/bin/bash

/usr/bin/supervisord
touch /tmp/output
sleep 5

mvn -Dmaven.repo.local=/root/lib tomcat7:run -Dmaven.tomcat.port=8000 -Dspring.profiles.active=prod -DwithGitHistoryServer=true -Djava.security.egd=file:/dev/./urandom -DskipTests > /tmp/output 2>&1 &

__started=false
while [ "$__started" == "false" ]
do
  echo "waiting for dendrite startup and build initial graph..."
  __lastline=$(tail /tmp/output -n 1)
  echo -e "startup message: $__lastline\n"

  if [[ "$__lastline" == *"INFO: Starting ProtocolHandler [\"http-bio-8000\"]"* ]]; then
    __started=true
  else
    sleep 5
  fi
done
