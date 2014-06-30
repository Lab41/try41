#!/bin/bash

untilsuccessful () {
        "$@"
        while [ $? -ne 0 ]; do
                echo Retrying...
                sleep 1
                "$@"
        done
}

if [ -z "$SSL" ]; then
	PORT=$(curl --silent http://172.17.42.1:2375/containers/$HOSTNAME/json | jq '.HostConfig.PortBindings."9200/tcp"[].HostPort' | sed "s/\"//g") 
	sed "s/location.port/$PORT/" -i /kibana/src/config.js
else
	sed "s/location.port/443/" -i /kibana/src/config.js
	sed "s|\"/\"|\"/hemlock2\"|" -i /kibana/src/config.js
	sed "s/http/https/" -i /kibana/src/config.js
fi  

/usr/sbin/mysqld &
sleep 5

# update the elasticsearch config
ELASTICSEARCH_CLUSTER=`pwgen -0AB -1 12`
echo cluster.name: $ELASTICSEARCH_CLUSTER >> /etc/elasticsearch/elasticsearch.yml
echo couchbase.password: password >> /etc/elasticsearch/elasticsearch.yml
echo discovery.zen.ping.multicast.enabled: false >> /etc/elasticsearch/elasticsearch.yml
echo node.local: true >> /etc/elasticsearch/elasticsearch.yml
echo index.number_of_shards: 1 >> /etc/elasticsearch/elasticsearch.yml
echo index.number_of_replicas: 0 >> /etc/elasticsearch/elasticsearch.yml

mkdir /usr/rbin

echo "if [ -f ~/.bashrc ]; then" >> /etc/rbash_profile
echo "    . ~/.bashrc" >> /etc/rbash_profile
echo "fi" >> /etc/rbash_profile
echo PATH=/usr/rbin >> /etc/rbash_profile
echo export PATH >> /etc/rbash_profile
echo unset USERNAME >> /etc/rbash_profile

rm /home/docker/.bashrc
rm /home/docker/.profile
ln -s /etc/rbash_profile /home/docker/.bash_profile
chown root: /home/docker/.bash_logout /home/docker/.bash_profile

echo PATH=/usr/rbin >> /home/docker/.bashrc
echo export PATH >> /home/docker/.bashrc
echo export HEMLOCK_MYSQL_SERVER=localhost >> /home/docker/.bashrc
echo export HEMLOCK_MYSQL_USERNAME=root >> /home/docker/.bashrc
echo export HEMLOCK_MYSQL_DB=hemlock >> /home/docker/.bashrc
echo export HEMLOCK_MYSQL_PW=password >> /home/docker/.bashrc
echo export HEMLOCK_COUCHBASE_SERVER=localhost >> /home/docker/.bashrc
echo export HEMLOCK_COUCHBASE_BUCKET=hemlock >> /home/docker/.bashrc
echo export HEMLOCK_COUCHBASE_USERNAME=Administrator >> /home/docker/.bashrc
echo export HEMLOCK_COUCHBASE_PW=password >> /home/docker/.bashrc
echo export HEMLOCK_ELASTICSEARCH_ENDPOINT=127.0.0.1:9200 >> /home/docker/.bashrc
echo alias read='' >> /home/docker/.bashrc
echo alias ulimit='' >> /home/docker/.bashrc
echo alias typeset='' >> /home/docker/.bashrc
echo alias type='' >> /home/docker/.bashrc
echo alias source='' >> /home/docker/.bashrc
echo alias printf='' >> /home/docker/.bashrc
echo alias logout='' >> /home/docker/.bashrc
echo alias local='' >> /home/docker/.bashrc
echo alias let='' >> /home/docker/.bashrc
echo alias enable='' >> /home/docker/.bashrc
echo alias declare='' >> /home/docker/.bashrc
echo alias command='' >> /home/docker/.bashrc
echo alias builtin='' >> /home/docker/.bashrc
echo alias bind='' >> /home/docker/.bashrc
echo alias fg='' >> /home/docker/.bashrc
echo alias bg='' >> /home/docker/.bashrc
echo alias dirs='' >> /home/docker/.bashrc
echo alias jobs='' >> /home/docker/.bashrc
echo alias unset='' >> /home/docker/.bashrc
echo alias history='' >> /home/docker/.bashrc
echo alias set='' >> /home/docker/.bashrc
echo alias shopt='' >> /home/docker/.bashrc
echo alias export='' >> /home/docker/.bashrc
echo alias exit='' >> /home/docker/.bashrc
echo alias help='' >> /home/docker/.bashrc
echo alias pwd='' >> /home/docker/.bashrc
echo alias kill='' >> /home/docker/.bashrc
echo alias echo='' >> /home/docker/.bashrc
echo alias unalias='' >> /home/docker/.bashrc
echo "function read() { clear; }" >> /home/docker/.bashrc
echo "function ulimit() { clear; }" >> /home/docker/.bashrc
echo "function typeset() { clear; }" >> /home/docker/.bashrc
echo "function type() { clear; }" >> /home/docker/.bashrc
echo "function source() { clear; }" >> /home/docker/.bashrc
echo "function printf() { clear; }" >> /home/docker/.bashrc
echo "function logout() { clear; }" >> /home/docker/.bashrc
echo "function local() { clear; }" >> /home/docker/.bashrc
echo "function let() { clear; }" >> /home/docker/.bashrc
echo "function enable() { clear; }" >> /home/docker/.bashrc
echo "function declare() { clear; }" >> /home/docker/.bashrc
echo "function command() { clear; }" >> /home/docker/.bashrc
echo "function builtin() { clear; }" >> /home/docker/.bashrc
echo "function bind() { clear; }" >> /home/docker/.bashrc
echo "function fg() { clear; }" >> /home/docker/.bashrc
echo "function bg() { clear; }" >> /home/docker/.bashrc
echo "function dirs() { clear; }" >> /home/docker/.bashrc
echo "function jobs() { clear; }" >> /home/docker/.bashrc
echo "function unset() { clear; }" >> /home/docker/.bashrc
echo "function history() { clear; }" >> /home/docker/.bashrc
echo "function set() { clear; }" >> /home/docker/.bashrc
echo "function shopt() { clear; }" >> /home/docker/.bashrc
echo "function export() { clear; }" >> /home/docker/.bashrc
echo "function exit() { clear; }" >> /home/docker/.bashrc
echo "function help() { clear; }" >> /home/docker/.bashrc
echo "function pwd() { clear; }" >> /home/docker/.bashrc
echo "function kill() { clear; }" >> /home/docker/.bashrc
echo "function echo() { clear; }" >> /home/docker/.bashrc
echo "function alias() { clear; }" >> /home/docker/.bashrc
echo "function unalias() { clear; }" >> /home/docker/.bashrc
echo "function function() { clear; }" >> /home/docker/.bashrc
echo alias function='' >> /home/docker/.bashrc
echo alias alias='' >> /home/docker/.bashrc

ln -s /usr/local/bin/hemlock /usr/rbin/hemlock
ln -s /usr/bin/clear /usr/rbin/clear

echo "CREATE DATABASE hemlock;" | mysql -ppassword

# start elasticsearch
/usr/share/elasticsearch/bin/elasticsearch -Des.default.path.conf=/etc/elasticsearch
untilsuccessful curl -XPUT http://localhost:9200/_template/couchbase -d @/src/couchbase_template.json

# add index for elasticsearch
untilsuccessful curl -XPUT http://localhost:9200/hemlock -d @/src/couchbase_template.json

# start couchbase
couchbase-start
