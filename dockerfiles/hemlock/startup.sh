#!/bin/bash

untilsuccessful () {
        "$@"
        while [ $? -ne 0 ]; do
                echo Retrying...
                sleep 1
                "$@"
        done
}

# Add docker user and generate a random password with 12 characters that includes at least one capital letter and number.
DOCKER_PASSWORD=`pwgen -c -n -1 12`
echo User: docker Password: $DOCKER_PASSWORD
DOCKER_ENCRYPYTED_PASSWORD=`perl -e 'print crypt('"$DOCKER_PASSWORD"', "aa"),"\n"'`
useradd -m -d /home/docker -p $DOCKER_ENCRYPYTED_PASSWORD docker
sed -Ei 's/adm:x:4:/docker:x:4:docker/' /etc/group

# Set the default shell as bash for docker user.
chsh -s /bin/bash docker

#Set all the files and subdirectories from /home/docker with docker permissions.
chown -R docker:docker /home/docker/*

# start the tty webapp
cp /src/favicon.ico /node_modules/tty.js/static/favicon.ico
cp /src/index.html /node_modules/tty.js/static/index.html
cp /src/tty.js /node_modules/tty.js/bin/tty.js
chmod +x /node_modules/tty.js/bin/tty.js
su -c '/node_modules/tty.js/bin/tty.js --port 8000 --daemonize' - docker

/usr/sbin/mysqld &
sleep 5

# sets the admin password to 'mysql-server' which is accessible from the outside
echo "CREATE DATABASE hemlock;" | mysql -ppassword

# untar the data
chown -R docker /Hemlock

# update the elasticsearch config
ELASTICSEARCH_CLUSTER=`pwgen -0AB -1 12`
echo cluster.name: $ELASTICSEARCH_CLUSTER >> /etc/elasticsearch/elasticsearch.yml
echo couchbase.password: password >> /etc/elasticsearch/elasticsearch.yml
echo discovery.zen.ping.multicast.enabled: false >> /etc/elasticsearch/elasticsearch.yml
echo node.local: true >> /etc/elasticsearch/elasticsearch.yml
echo index.number_of_shards: 1 >> /etc/elasticsearch/elasticsearch.yml
echo index.number_of_replicas: 0 >> /etc/elasticsearch/elasticsearch.yml

# set env for docker user
ln -s /bin/bash /bin/rbash
ls -la /bin/rbash lrwxrwxrwx
mkdir /usr/rbin

echo "if [ -f ~/.bashrc ]; then" >> /etc/rbash_profile
echo "    . ~/.bashrc" >> /etc/rbash_profile
echo "fi" >> /etc/rbash_profile
echo PATH=/usr/rbin >> /etc/rbash_profile
echo export PATH >> /etc/rbash_profile
echo unset USERNAME >> /etc/rbash_profile

rm /home/docker/.bash_profile
rm /home/docker/.bashrc
rm /home/docker/.profile
ln -s /etc/rbash_profile /home/docker/.bash_profile
chown root: /home/docker/.bash_logout /home/docker/.bashrc /home/docker/.bash_profile

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

/home/docker/.bash_logout clear

ln -s /usr/local/bin/hemlock /usr/rbin/hemlock
ln -s /usr/bin/clear /usr/rbin/clear

sed -i s/bash/rbash/g /etc/passwd

# start elasticsearch
/usr/share/elasticsearch/bin/elasticsearch -Des.default.path.conf=/etc/elasticsearch
untilsuccessful curl -XPUT http://localhost:9200/_template/couchbase -d @/usr/share/elasticsearch/plugins/transport-couchbase/couchbase_template.json

# start couchbase
couchbase-start

# add index for elasticsearch
untilsuccessful curl -XPUT 'http://localhost:9200/hemlock/'

# serve up directory for images, TODO
cd /; python -m SimpleHTTPServer 8080
