#!/bin/bash

/usr/bin/supervisord
sleep 2
mvn -Dmaven.repo.local=/root/lib tomcat7:run -Dmaven.tomcat.port=8000 -Dspring.profiles.active=prod -DwithGitHistoryServer=true -Djava.security.egd=file:/dev/./urandom -DskipTests > /tmp/output 2>&1 &

tail -f /tmp/output | while read LOGLINE
do
   [[ "${LOGLINE}" == *"INFO: Starting ProtocolHandler [\"http-bio-8000\"]"* ]] && pkill -P $$ tail
done

tail -f /tmp/output | while read LOGLINE
do
   [[ "${LOGLINE}" == *"INFO: Starting ProtocolHandler [\"http-bio-8000\"]"* ]] && pkill -P $$ tail
done
