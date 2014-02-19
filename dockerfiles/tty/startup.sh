#!/bin/bash

# Add docker user and generate a random password with 12 characters that includes at least one capital letter and number.
DOCKER_PASSWORD=`pwgen -c -n -1 12`
echo User: docker Password: $DOCKER_PASSWORD
DOCKER_ENCRYPYTED_PASSWORD=`perl -e 'print crypt('"$DOCKER_PASSWORD"', "aa"),"\n"'`
useradd -m -d /home/docker -p $DOCKER_ENCRYPYTED_PASSWORD docker
sed -Ei 's/adm:x:4:/docker:x:4:docker/' /etc/group

# Set the default shell as bash for docker user.
chsh -s /bin/bash docker

# Copy the config files into the docker directory
cd /src; tar -C /home/docker -xvf config.tar

#Set all the files and subdirectories from /home/docker with docker permissions.
chown -R docker:docker /home/docker/*

# start the tty webapp
cp /src/tty.js /node_modules/tty.js/bin/tty.js
chmod +x /node_modules/tty.js/bin/tty.js
su -c '/node_modules/tty.js/bin/tty.js --port 8000 --daemonize' - docker

# serve up directory for images, TODO
cd /home/docker; python -m SimpleHTTPServer 8080
